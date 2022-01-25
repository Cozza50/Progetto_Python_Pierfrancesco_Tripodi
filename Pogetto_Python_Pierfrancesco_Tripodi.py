import requests
import time
from datetime import datetime
import schedule

class Report:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'd6c261ac-1898-4ff3-b231-fd500b4a46ff'
        }

        self.list = []

    def fetch_currencies_data(self):
        r = requests.get(url=self.url, params=self.params, headers=self.headers).json()
        return r['data']

def work():
    now = datetime.now()
    base_report = Report()
    all_data = base_report.fetch_currencies_data()

#1) La criptovaluta con il volume maggiore nelle ultime 24 ore.
    best_volume = None 
    
    for x in all_data:
        if not best_volume or x['quote']['USD']['volume_24h'] > best_volume['quote']['USD']['volume_24h']:
            best_volume = x
            symbol = x['symbol']
            volume = x['quote']['USD']['volume_24h']
            max_vol_24 = {
                'La criptovaluta con il volume maggiore nelle ultime 24 ore': {
                f'{symbol}': volume
                }
            }
    base_report.list.append(max_vol_24)

#2) Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore).
    all_incremento = {}
    
    for x in all_data:
        s = x['symbol']
        p = x['quote']['USD']['percent_change_24h']
        all_incremento[f'{s}'] = p
    ordered_incremento = sorted((value, key) for (key,value) in all_incremento.items())
    min_incremento = ordered_incremento[0:10]
    diz_min_inc = {}
    
    for x in min_incremento:
        diz_min_inc[f'{x[1]}'] = x[0]
    max_incremento = ordered_incremento[-10:]
    diz_max_inc = {}
    
    for x in max_incremento:
        diz_max_inc[f'{x[1]}'] = x[0]

    diz_incremento = {
        'Le 10 migliori': diz_max_inc,
        'Le 10 peggiori': diz_min_inc
    }
    diz_inc = {'Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)': diz_incremento}
    base_report.list.append(diz_inc)


#3)La quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute.
    cap = {}
    for x in all_data:
        s = x['symbol']
        i = x['quote']['USD']['market_cap']
        cap[f'{s}'] = i
    ordered_cap = sorted((value, key) for (key,value) in cap.items())
    top_20_coin = ordered_cap[-20:]
    chiavi = []
    
    for x in top_20_coin:
        p = x[1]
        chiavi.append(p)
    diz_price = {}
   
    for x in all_data:
        if x['symbol'] in chiavi:
            a = x['symbol']
            b = x['quote']['USD']['price']
            diz_price[f'{a}'] = b
    total_cash = sum(diz_price.values())
    total_cash_diz = {'Quantita per acquistare una unita di ciascuna delle prime 20 criptovalute per capitalizzazione, in $': total_cash}
    base_report.list.append(total_cash_diz)


#4)La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume
#delle ultime 24 ore sia superiore a 76.000.000$:

    diz_unita = {}

    for x in all_data:
        if x['quote']['USD']['volume_24h'] > 76000000:
            simbolo = x['symbol']
            prezzo_unita = x['quote']['USD']['price']
            diz_unita[f'{simbolo}'] = prezzo_unita
    somma = sum(diz_unita.values())
    prezzo_somma = {'Quantita per acquistare una unita di ogni criptovaluta con capitalizzazione superiore a 76.000.000, in $': somma}
    base_report.list.append(prezzo_somma)


#5)La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna
#delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca non sia cambiata):

    diz_prezzi_ieri = {}
    for x in all_data:
        if x['symbol'] in chiavi:
            xs = x['symbol']
            prezzo_now = x['quote']['USD']['price']
            incremento = x['quote']['USD']['percent_change_24h']

            z = 100 + incremento
            prezzo_ieri_singola = 100*prezzo_now/z

            diz_prezzi_ieri[f'{xs}'] = prezzo_ieri_singola

    somma_prezzo_ieri = sum(diz_prezzi_ieri.values())

    differenza_prezzi = total_cash - somma_prezzo_ieri
    incremento_percentuale = differenza_prezzi * 100 / somma_prezzo_ieri

    incremento_percentuale_diz = {'La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unita di ciascuna delle prime 20 criptovalute (per capitalizzazione) il giorno prima (ipotizzando classifica invariata)': incremento_percentuale}
    base_report.list.append(incremento_percentuale_diz)


    

    #JSON
    data_oggi = now.strftime('%m%d%y')
    import json
    with open(f"{data_oggi}.json", "w") as outfile:
        json.dump(base_report.list, outfile, indent=4)

   

#CICLO:
schedule.every().day.at("10:00").do(work)
while True:
    work()
    time.sleep(1)