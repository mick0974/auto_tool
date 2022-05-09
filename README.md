# Automated format string exploit tool
Questo tool etc etc

## Format string exploit
La vulnerabilità di format string sfrutta un cattivo uso, da parte del programmatore, delle funzioni di stampa in un determinato linguaggio di programmazione.
Per semplicità nei seguenti esempi prenderemo in considerazione, in particolare, il caso della funzione printf in C, ma questo exploit è applicabile anche in altri linguaggi e con diverse funzioni di stampa.
La funzione printf, quando viene specificato un elemento di formattazione come %s, effettua un pop dello stack, interpreta il valore ottenuto come stringa e lo sostituisce a tempo di compilazione a %s per stamparlo. In un caso come _printf("val1: %d, val2: %d, val3: %d", n1, n2, n3)_ i valori n1, n2 ed n3 vengono aggiunti nello stack sopra la funzione di stampa, e printf effettua 3 pop per recuperarli, interpretarli come decimali e stamparli a video. In un caso invece come _printf("val1: %d")_ in cui non è stato specificato alcun argomento, printf effettua comunque un pop dello stack andando a recuperare il primo valore successivo presente nello stack, leggendo memoria che non era in origine destinata ad essa.
Supponiamo ora che all'utente venga consentito di assegnare un valore a una stringa di nome _userinput_ attraverso una funzione scanf, e che questa stringa venga poi fornita come input diretto per una printf con _printf(userinput)_, nel caso in cui l'utente inserisca _"%d %d %d"_ la funzione printf interpreterà i 3 %d come caratteri di formattazione, stampando a video i 3 elementi successivi dello stack. In una situazione come questa l'utente ha completa libertà di leggere il contenuto della memoria del programma semplicemente aggiungendo ulteriori %d al suo input.

### Leggere la memoria di un programma
Come abbiamo visto nell'esempio precedente, è possibile leggere memoria da qualsiasi posizione dello stack sfruttando una sequenza di formattatori, ma è anche possibile utilizzare la sintassi di direct parameter access per accedere direttamente alla posizione desiderata dello stack usando $n%y, dove n è l'offset rispetto alla posizione attuale sullo stack dell'indirizzo target e y è il tipo in cui formattare il valore ottenuto. Ad esempio $5%x stamperà il valore trovato a distanza 5 sullo stack come valore esadecimale: questo tipo di accesso risulta possibile con la maggior parte delle librerie C e semplifica notevolmente l'exploit. Questo tool utilizza il direct parameter access per effettuare l'exploit, poiché la scrittura automatizzata di determinati valori a determinati indirizzi senza di esso risulterebbe troppo complessa e spesso impossibile.

### Scrivere valori usando printf
