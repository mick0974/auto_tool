# Automated format string exploit tool
Questo tool etc etc

## Format string exploit
La vulnerabilità di format string sfrutta un cattivo uso, da parte del programmatore, delle funzioni di stampa in un determinato linguaggio di programmazione.
Per semplicità nei seguenti esempi prenderemo in considerazione, in particolare, il caso della funzione printf in C, ma questo exploit è applicabile anche in altri linguaggi e con diverse funzioni di stampa.
La funzione printf, quando viene specificato un elemento di formattazione come %s, effettua un pop dello stack, interpreta il valore ottenuto come stringa e lo sostituisce a tempo di compilazione a %s per stamparlo. In un caso come _printf("val1: %d, val2: %d, val3: %d", n1, n2, n3)_ i valori n1, n2 ed n3 vengono aggiunti nello stack sopra la funzione di stampa, e printf effettua 3 pop per recuperarli, interpretarli come decimali e stamparli a video. In un caso invece come _printf("val1: %d")_ in cui non è stato specificato alcun argomento, printf effettua comunque un pop dello stack andando a recuperare il primo valore successivo presente nello stack, leggendo memoria che non era in origine destinata ad essa.
Supponiamo ora che all'utente venga consentito di assegnare un valore a una stringa di nome _userinput_ attraverso una funzione scanf, e che questa stringa venga poi fornita come input diretto per una printf con _printf(userinput)_, nel caso in cui l'utente inserisca _"%d %d %d"_ la funzione printf interpreterà i 3 %d come caratteri di formattazione, stampando a video i 3 elementi successivi dello stack. In una situazione come questa l'utente ha completa libertà di leggere il contenuto della memoria del programma semplicemente aggiungendo ulteriori %d al suo input.

### Leggere la memoria di un programma
Come abbiamo visto nell'esempio precedente, è possibile leggere memoria da qualsiasi posizione dello stack sfruttando una sequenza di formattatori, ma è anche possibile utilizzare la sintassi di direct parameter access per accedere direttamente alla posizione desiderata dello stack usando $n%y, dove n è l'offset rispetto alla posizione attuale e y è il tipo in cui formattare il valore ottenuto: ad esempio $5%x stamperà il valore trovato a distanza 5 sullo stack come valore esadecimale. Questo tipo di accesso risulta possibile con la maggior parte delle librerie C e semplifica notevolmente l'exploit. Questo tool utilizza il direct parameter access, poiché la scrittura automatizzata di determinati valori a determinati indirizzi senza di esso risulterebbe molto complessa e più frequentemente impossibile.

### Scrivere valori in memoria usando printf
Fra i formattatori di stampa ne esiste uno molto particolare: %n recupera il prossimo argomento dello stack, lo interpreta come indirizzo di memoria e scrive a quell'indirizzo il numero di caratteri stampati fino a quel momento. Questo formattatore permette quindi di effettuare un exploit che scriva valori arbitrari nella memoria del programma, fintanto che l'indirizzo a cui scrivere è presente sullo stack e raggiungibile con una sequenza di pop o con direct parameter access.
Nel caso in cui l'indirizzo non sia presente in memoria spesso è possibile specificarlo: potremmo ad esempio usare la stessa scanf con cui inseriamo formattatori per inserire anche l'indirizzo a cui desideriamo scrivere: specificando _"AAAA $32%p \x25\x25\x25\x25"_, supponendo che 32 sia l'offset necessario a raggiungere la stringa che abbiamo specificato ed è salvata sullo stack, stamperemo l'indirizzo di memoria 0x25252525. Scrivendo invece _"AAAA $32%n \x25\x25\x25\x25"_ scriveremo il valore 5 (poiché prima di %x abbiamo stampato _"AAAA "_ di lunghezza 5) all'indirizzo 0x25252525.
Un aspetto importante da ricordare è che nel caso di architettura a 64 bit gli indirizzi conterranno spesso più null byte \x00, che verranno interpretati dalla printf come caratteri di terminazione della stringa ed interromperanno la stampa: per ovviare a questo problema è sufficiente appendere gli indirizzi a cui scrivere al termine della stringa, così che non impediscano la stampa dei caratteri necessari a raggiungere il valore che si vuole scrivere in memoria.
Un altro aspetto da considerare è il fatto che il programmatore potrebbe aggiungere un limite al numero di caratteri salvati dalla funzione di input: è possibile limitare la possibilità di incorrere in questo problema stampando i caratteri necessari usando, ad esempio, un _%300d_ piuttosto che passando 300 caratteri di padding.
Infine è importante ricordare che la printf non garantisce la stampa di più di 4095 caratteri: per non incorrere in problemi di questo tipo il tool spezza la singola scrittura in più sottoscritture (come specificato di seguito) fino a quando la somma dei singoli sottovalori non risulta minore di 4000.
