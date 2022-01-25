### In cosa consiste 
Il progetto è un programma assegnato da Start2Impact. Esso utilizza l'API offerta da CoinMarketCap, per ricevere dati su tutte le criptovalute
del mercato, analizzandoli e estraendo delle informazioni.
Nello specifico esso permette di scoprire:
- la criptovaluta che avesse il volume maggiore nelle ultime 24 ore
- la quantità di denaro necessaria per acquistare un'unità di tutte le prime 20 criptovalute per capitalizzazione
- la percentuale di denaro guadagnata se si vendessero oggi le prime 20 criptovalute acquistate ieri
- La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
- le migliori e le peggiori 10 criptovalute per incremento percentuale nelle ultime 24h

### Cosa serve per provarlo 
1) Creare con python un ambiente virtuale 
2) Installare al suo interno la libreria 'requests' tramite pip
3) Richiedere una chiave API al link raggiungibile [qui](https://pro.coinmarketcap.com/)
4) Inserire l'API ottenuta nel 'main.py' alla riga 21 al posto di '---- API KEY HERE ----'
5) Crea nella stessa directory del file 'main.py' una nuova cartella chiamata 'jsonData'
6) Fai partire il programma

Esso mostrerà alcuni dati sul terminale e andrà a creare un file Json nella nuova cartella, dove saranno elencate in maniera precisa tutte le informazioni.
