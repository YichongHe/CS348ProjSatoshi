import cryptocompare
import requests
import json
import csv
import datetime

#set api key
apikey = '6bfaec6ae1a1086dfcf4662621b6ed57b0c19fa60dc119fca3eb1e3c1eb08e01'
cryptocompare.cryptocompare._set_api_key_parameter(apikey)

#print(cryptocompare.get_historical_price('XMR', 'EUR', datetime.datetime(2017,6,6)))
#print(cryptocompare.get_historical_price('XMR', timestamp=datetime.datetime(2017,6,6), exchange='CCCAGG'))
#pairs_cb = cryptocompare.get_pairs(exchange = "Coinbase")
exchanges = cryptocompare.get_exchanges()

#print(pairs_cb[0]['tsym'])
"""
for i = 0 to pairs_cb.size()
    if pairs_cb[i]['tsym'] == 'USD'
        print(paris_cb[i]['tsym']

"""
#print(exchanges)
#print(exchanges.keys())
#print(exchanges['Coinbase'].keys())

#attach to end of URLstring
url_api_part = '&api_key=' + apikey

URLcoinslist = 'https://min-api.cryptocompare.com/data/all/exchanges'

#Get list of cryptos with their symbols
"""res1 = requests.get(URLcoinslist)
res1_json = res1.json()
data1 = res1_json['Data']
symbol_array = []
cryptoDict = dict(data1)"""

#write to CSV
with open('exch_names.csv', mode = 'w') as test_file:
   test_file_writer = csv.writer(test_file, 
                                 delimiter = ',', 
                                 quotechar = '"', 
                                 quoting=csv.QUOTE_MINIMAL)
   for exchange in exchanges.values():
       name = exchange['Name']
       Id = exchange['Id']
       country = exchange['Country']
       url = exchange['AffiliateURL']
       #rating = exchange['Rating']
       entry = [name, Id, url, country]
       test_file_writer.writerow(entry)
print('Done with Exchanges')


#coins = cryptocompare.get_coin_list(format=False)['BTC']
coins = cryptocompare.get_coin_list(format=False)
with open('coin_names.csv', mode = 'w') as coin_file:
   coin_file_writer = csv.writer(coin_file, 
                                 delimiter = ',', 
                                 quotechar = '"', 
                                 quoting=csv.QUOTE_MINIMAL)
   for keys in coins.keys():
     name = coins[keys]['CoinName']
     Id = coins[keys]['Id']
     algorithm = coins[keys]['Algorithm']
     prooftype = coins[keys]['ProofType']
     entry = [name, Id, algorithm, prooftype]
     coin_file_writer.writerow(entry)
print('Done with Coins')
