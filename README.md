# Auto format string tool
Auto format string tool è un tool scritto in python che, sfruttando una vulnerabilità format string presente nel programma target, calcola la stringa con padding necessaria per la scrittura di un valore ad uno specifico indirizzo di memoria.  
Per il corretto funzionamento del tool è richiesto che meccanismi di sicurezza come stack protector e ASLR siano disabilitati, così che sia possibile calcolare il padding corretto attraverso più esecuzioni del programma target.  

## Format string exploit
La vulnerabilità di format string sfrutta un cattivo uso, da parte del programmatore, delle funzioni di output o stampa che consentono la formattazione di valori.
Per semplicità nei seguenti esempi prenderemo in considerazione, in particolare, il caso della funzione printf in C, ma questo exploit è applicabile anche in altri linguaggi di programmazione e con diverse funzioni di stampa.  
La funzione printf, quando viene specificato un elemento di formattazione come _%s_, effettua un pop dello stack, interpreta il valore ottenuto come stringa e lo sostituisce a tempo di compilazione a _%s_ per stamparlo. In un caso come _printf("val1: %d, val2: %d, val3: %d", n1, n2, n3)_ i valori n1, n2 ed n3 vengono aggiunti nello stack sopra la funzione di stampa, e printf effettua 3 pop per recuperarli, interpretarli come decimali e stamparli a video. In un caso invece come _printf("val1: %d")_ in cui non è stato specificato alcun argomento, printf effettua comunque un pop dello stack recuperando il valore successivo dello stack, leggendo memoria che non era in origine destinata ad essere stampata.  
Supponiamo ora che all'utente venga consentito di assegnare un valore a una stringa di nome _userinput_ attraverso una funzione scanf, e che questa stringa venga poi fornita come input diretto per una printf con _printf(userinput)_, nel caso in cui l'utente inserisca _"%d %d %d"_ la funzione printf interpreterà i 3 %d come caratteri di formattazione, stampando a video i 3 elementi successivi dello stack. In una situazione come questa l'utente ha completa libertà di leggere il contenuto della memoria del programma aggiungendo un quantitativo di %d a piacere.

### Leggere la memoria di un programma
Come abbiamo visto nell'esempio precedente, è possibile leggere la memoria di un programma sfruttando una sequenza di formattatori, ma è anche possibile utilizzare la sintassi di direct parameter access per accedere direttamente alla posizione desiderata dello stack: usando $n%y, dove n è l'offset rispetto alla posizione attuale e y è il tipo in cui formattare il valore ottenuto, riusciremo a leggere un indirizzo di memoria senza dover prima effettuare pop degli elementi che lo precedono; ad esempio $5%x stamperà il valore trovato a distanza 5 sullo stack come valore esadecimale.  
Questo tipo di accesso risulta possibile con la maggior parte delle librerie C e semplifica notevolmente l'exploit: questo tool utilizza il direct parameter access, poiché la scrittura automatizzata di un valore arbitrario a un determinato indirizzo senza di esso risulterebbe molto complessa e più frequentemente impossibile.

### Scrivere valori in memoria usando printf
Fra i formattatori di stampa ne esiste uno molto particolare: %n recupera il prossimo argomento dello stack, lo interpreta come indirizzo di memoria e scrive a quell'indirizzo il numero di caratteri stampati a video fino a quel momento. Questo formattatore permette quindi di effettuare un exploit che scriva valori arbitrari nella memoria del programma a condizione che l'indirizzo a cui scrivere sia presente sullo stack e sia raggiungibile con una sequenza di pop o con direct parameter access.
Nel caso in cui l'indirizzo a cui si desidera scrivere non sia presente in memoria è comunque possibile specificarlo: potremmo ad esempio usare la stessa scanf con cui inseriamo formattatori per inserire l'indirizzo a cui desideriamo scrivere; specificando _"AAAA $32%p \x25\x25\x25\x25"_, supponendo che 32 sia l'offset necessario a raggiungere i byte dell'indirizzo contenuti nella stringa che abbiamo specificato, stamperemo 0x25252525. Scrivendo invece _"AAAA $32%n \x25\x25\x25\x25"_ scriveremo il valore 5 (poiché prima di %x abbiamo stampato _"AAAA "_ di lunghezza 5) all'indirizzo di memoria 25252525.  
Un aspetto importante da ricordare è che nel caso di architettura a 64 bit gli indirizzi conterranno spesso uno o più null byte _\x00_, che verranno interpretati dalla printf come caratteri di terminazione della stringa ed interromperanno la stampa: per evitare di incorrere in questo problema è sufficiente appendere gli indirizzi a cui scrivere al termine della stringa di exploit, così che non impediscano la stampa dei caratteri necessari a raggiungere il valore che si desidera scrivere.
Un altro aspetto da considerare è il fatto che il programmatore potrebbe aggiungere un limite massimo al numero di caratteri accettati dalla funzione di input: è possibile ridurre la probabilità di incorrere in questo problema specificando, ad esempio, un _%300d_ piuttosto che passando 300 caratteri di padding.
Infine è importante ricordare che la printf non garantisce la stampa di più di 4095 caratteri: per non incorrere in problemi di questo tipo il tool spezza la singola scrittura in più sottoscritture (come specificato di seguito) fino a quando la somma dei singoli sottovalori non risulta minore di 4000.


## Algoritmi impiegati

### Formattazione dei valori in byte
Il tool decide i parametri con cui i valori verranno formattati in byte:  
**Endianess**: _<_ per little endian, _>_ per big endian o stringa vuota se non specificata (viene impiegata quella del processore in uso).  
**Byte size**: _Q_ per 8, _L_ per 4, _H_ per 2, _B_ per 1.

### Decisione della write size
Il tool, per evitare di superare il limite superiore di caratteri di stampa garantiti dalla printf, spezza il valore da scrivere in più sottovalori, fino a che la loro somma non è inferiore a 4000.  
Partendo dalla dimensione di scrittura originale, il tool itera più volte spezzando ad ogni ciclo il sottovalore massimo nella dimensione di scrittura successiva (in ordine decrescente 8, 4, 2 e 1): un valore esadecimale come _0x003f0046_ pari a 4128838 verrebbe spezzato in _0x003f_ pari a 63 e _0x0046_ pari a 70, e l'iterazione terminerebbe con i sottovalori _0x003f_ e _0x0046_ poiché la loro somma 133 risulterebbe minore di 4095.

### Test preliminari sugli input
Per prima cosa il tool controlla se ha il permesso di modificare l'input che sta testando, altrimenti lo scarta.
Dopodiché nel caso in cui l'input corrente sia passato come argomento da linea di comando e gli indirizzi a cui scrivere contengano null byte questo viene scartato (poiché il null byte viene usato per separare gli input di argv e l'exploit risulta impossibile).
Si verifica quindi se l'input è exploitabile inserendo come input un %p e verificando che il numero di %p non sia aumentato e che il numero di 0x sia incrementato solamente di uno.  
Supponendo di aver superato questo test, viene creata una stringa random lunga quanto la somma della lunghezza in caratteri degli indirizzi target, il padding necessario a raggiungere il valore da scrivere in ciascun indirizzo e il relativo scrittore (hhn, hn, n, ln).
Questa stringa viene passata in input al processo e si verifica se è presente nella sua risposta: se essa non è presente e il controllo sulla lunghezza è specificato come attivo nel file di configurazione del tool allora l'input viene scartato, altrimenti si procede.
Dopodiché vengono determinati i due marcatori unici per la risposta: i marcatori sono due stringhe non ripetute nella risposta che semplificano l'estrazione dell'input.  
I marcatori hanno una lunghezza minima di 2 caratteri e massima di 50: per ogni lunghezza si effettuano fino a 200 tentatividi creazione, nel caso in cui il tool non riesca a creare marcatori non ripetuti nella risposta l'input viene scartato.
Una volta definiti i marcatori, il tool dà una stima sulla dimensione dell'input calcolandone la dimensione fino a 500 + lunghezza dei marcatori + numero di caratteri usati per il controllo sulla lunghezza.

### Calcolo della posizione nello stack
Per la ricerca possono essere utilizzate 3 stringhe diverse:
1. Marcatore sinistro + pattern da ricercare + posizioni (serie di %N$p per N >= 0) + padding (di lunghezza variabile per raggiungere la lunghezza dell'input) + marcatore destro.  
2. In caso di segmentation fault, viene inizialmente usata una stringa alternativa con soli due %N$p all'interno delle posizioni: il numero di %N$p viene incrementato ad ogni esecuzione fino a trovare l'input (in caso di un altro segmentation fault la ricerca termina e si passa all'input successivo).   
3. Questa stringa viene usata per gestire le snprintf in caso la stringa di exploit sia passata come argv: in questo caso particolare argv viene subito interpretato e poi salvato nella variabile di destinazione, dunque ogni %N$p avrà una lunghezza diversa (al più 18 caratteri, "0x" + valore) legata al valore esadecimale stampato. Di conseguenza supponiamo che ogni %N$p sia grande 18 caratteri e creiamo la stringa di conseguenza, per il resto analoga alle due forme precedenti.

### Verifica della posizione nello stack
La stringa viene quindi associata all'input corrente e si procede con i test.  
Il pattern da ricercare all'interno dello stack può essere spezzato in due entry successive o lasciato intero. Una volta individuata ogni posizione del pattern si procede a verificare la correttezza di queste: i caratteri del pattern vengono sostituiti con altri caratteri.  
Assumendo a questo punto che la posizione sia corretta, questa viene salvata e viene ritornato il numero di caratteri di padding necessari ad allineare il pattern alla posizione successiva.

### Creazione stringa finale
La forma della stringa finale è:  
1. padding (di lunghezza pari al valore da scrivere)
2. posizione nello stack dell'indirizzo a cui scrivere
3. (1) e (2) vengono ripetuti in serie a seconda del numero di scritture necessarie
4. serie di indirizzi a cui scrivere
5. padding finale per rispettare la dimensione degli input  

Alcune considerazioni sulla stringa finale:  
- con l'algoritmo precedente abbiamo determinato la posizione di partenza della format string all'interno dello stack: a partire da quel valore ricalcoliamo un'ultima volta la posizione nello stack degli indirizzi per la parte (2) aggiungendo un offset fisso.
- la parte (5), cioè il padding finale, è presente solo nel caso in cui gli input siano passati attraverso argv.
- nel caso in cui l'input sia specificato a tempo di esecuzione (ad esempio in risposta ad una scanf) il marcatore sinistro e l'input di allineamento non vengono anteposti alla stringa finale poiché gli input raccolti a runtime, a differenza di argv, sono allineati rispetto agli indirizzi dello stack e la presenza di un marker sinistro li sposterebbe.
- nel caso in cui l'input sia specificato come argv è necessario controllare se il numero di caratteri di padding di allineamento ritornato dall'algoritmo precedente sommato alla lunghezza del marcatore sinistro sia uguale alla dimensione degli indirizzi (4 o 8 byte).
  In caso di uguaglianza non è necessario anteporre nè il marcatore nè il padding di allineamento rispetto ad esso, in caso contrario si mantiene il marcatore e si aggiunge il corrispettivo padding.  

Una volta generata la stringa finale questa viene testata:  
1. nel caso in cui il processo termini correttamente il tool suppone che l'exploit sia andato a buon fine e riporta la risposta ricevuta dal processo.
2. nel caso in cui il processo termini con un segmentation fault il tool ritenta l'exploit ricostruendo la stringa in modo differente solo se nessun indirizzo contiene un null byte (altrimenti l'exploit risulta impossibile):

   1. serie di indirizzi a cui scrivere
   2. padding (di lunghezza pari al valore da scrivere)
   3. posizione nello stack dell'indirizzo a cui scrivere (ricalcolata in base alla nuova forma della stringa)
   4. (1) e (2) vengono ripetuti in serie a seconda del numero di scritture necessarie
   5. padding finale per rispettare la dimensione degli input

  dove la lunghezza del padding del punto (2) viene ridotta della lunghezza degli indirizzi; nel caso in cui il padding sia più corto degli indirizzi l'exploit risulta impossibile.  
  Nel caso in cui l'input sia specificato a tempo di esecuzione (ad esempio in risposta ad una scanf) il marcatore sinistro e il padding di allineamento non vengono anteposti alla stringa finale poiché gli input raccolti a runtime, a differenza di argv, sono allineati rispetto agli indirizzi dello stack e la presenza di un marker sinistro li sposterebbe.  
  Nel caso in cui l'input sia specificato come argv è necessario controllare se il numero di caratteri di padding di allineamento ritornato dall'algoritmo precedente sommato alla lunghezza del marcatore sinistro sia uguale alla dimensione degli indirizzi (4 o 8 byte).  
  In caso di uguaglianza non è necessario anteporre nè il marcatore nè il padding di allineamento rispetto ad esso, in caso contrario si mantiene il marcatore, si aggiunge il corrispettivo padding e si riduce la lunghezza dei padding del punto (2) della lunghezza di questi.  
   
  Se il processo termina correttamente il tool suppone che l'exploit sia andato a buon e riporta la risposta ricevuta dal processo, altrimenti in caso di segmentation fault l'exploit risulta impossibile.  


## Parametri accettati e configurazione
### Parametri
Il tool accetta i seguenti parametri da linea di comando:
- **target**: path relativo del programma target su cui effettuare l'exploit
- **target_address**: indirizzo target del programma su cui effettuare la scrittura, è interpretato come valore decimale o esadecimale se preceduto da _0x_
- **target_value**: valore da scrivere al target_address, è interpretato come valore decimale o esadecimale se preceduto da _0x_
- **input_file**: path relativo del file json contenente gli input da passare al programma target

### File di input
Il file di input json è strutturato nel seguente modo:

_{
  "input": [
    {
      "type": ...,
      "marker": ...,
      "value": ...
    },
    ...
  ]
}_

Gli input sono contenuti in un array salvato con chiave _input_, e sono strutturati con i seguenti campi:
- **type**: tipo dell'input, _command_line_input_ se passato da linea di comando o _execution_input_ se passato a tempo di esecuzione
- **marker**: risposta in stampa dal programma target attesa, non specificato nel caso di input passato da linea di comando
- **value**: input da passare al programma target

### File di configurazione
- **bytes_to_write**: il numero di byte da scrivere al target_address
- **wait_time_marker**: tempo di attesa in caso di uso di marker quando l'input è passato a tempo di esecuzione
- **wait_time_no_marker**: tempo di attesa in caso di assenza di marker prima di inviare il prossimo input
- **log_dir**: path relativo del file di log
- **input_len_control**: permette di specificare se permettere al controllo sul numero di caratteri di input di bloccare il processo o meno
