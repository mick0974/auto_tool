# Auto format string tool
Auto format string tool è un tool scritto in python che, sfruttando una vulnerabilità format string presente nel programma target, calcola la stringa con padding necessaria per la scrittura di un valore ad uno specifico indirizzo di memoria.  
Per il corretto funzionamento del tool è richiesto che meccanismi di sicurezza come stack protector e ASLR siano disabilitati, così che sia possibile calcolare il padding corretto attraverso più esecuzioni del programma target.  

## Requisiti
 - python 3.6
 - pwntools 4.6

## Funzionamento
Il tool può essere eseguito da line di comando con:

    python main.py taget target_address target_value input_file

La carella **test** contiene alcuni programmi C con cui testare il tool. Per ciascun programma è presente il relativo file di input .json e un file compile.sh che contiene il comando, con relativi parametri, usato per compilare il codice durante i nostri test.

La cartella **results** contiene un esempio di file fi log generati dal tool per i vari programmi di test.

Il file **test.sh** contiene il comando di esecuzione del tool adattato per i vari programmi di test (supponendo che il binario sia già stato compilato). Sarà ovviamente necessatio modificare il valore associato a target_address (eccetto per the_answer). 

A questo riguardo:
- commandline.c -> variabile a cui scrivere: _target_, usare indirizzo a tempo di esecuzione
- secret_number.c -> variabile a cui scrivere: _secret_num_
- simil_stonks.c -> variabile a cui scrivere: _target_
- snprintf1.c -> variabile a cui scrivere: _i_, usare indirizzo a tempo di esecuzione
- snprintf3.c -> variabile a cui scrivere: _i_
- test1.c -> variabile a cui scrivere: _twentythree_
- vuln.c -> variabile a cui scrivere: _target_

Per i programmi in cui è specificato che l'indirizzo da usare a tempo di esecuzione, è stato fatto in modo che questo venga stampato con una printf(). In tutti gli altri casi, Eccetto per dove diversamente specificato, l'indirizzo della variabile a cui scrivere può essere ottenuto con _objdump -t binario_.