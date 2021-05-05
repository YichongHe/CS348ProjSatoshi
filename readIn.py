import cryptocompare as crt
import numpy as np
import pandas as pd
from mysql.connector import connect, Error



mydbs = connect(
    host="localhost",
    user="he463",
    password="85719712")

#create cursor and empty database
cursor = mydbs.cursor()
cursor.execute("""create database if not exists Satoshi""")
cursor.execute("""use Satoshi""")

crt.cryptocompare._set_api_key_parameter("d689d2184dacdafb92a49f248114de4d764a2af5c0b284fdfb42e05947be06b9")

def loadPriceData():
    
    coin_list = crt.get_coin_list()
    keys = list(coin_list.keys())
    
    
    coin_data = {}
    for keyIndex in range(len(keys)):
        if not coin_list[keys[keyIndex]]['Rating']['Weiss']['Rating']:
            del coin_list[keys[keyIndex]]
        else:
            price_list = crt.get_price(keys[keyIndex], currency='USD', full=True)
            if price_list:
                coin_data.update(price_list['RAW'])
            keyIndex = keyIndex+1
    
    for k in coin_data.keys():
        coin_data[k] = coin_data[k]['USD']
        
        
    coin_data = pd.DataFrame.from_dict(coin_data, orient='index') 
    
    return coin_data[['FROMSYMBOL', 'PRICE', 'MKTCAP', 'VOLUME24HOURTO', 'SUPPLY', 'IMAGEURL']]
    
    
def loadCoinData():
    
    coin_list = crt.get_coin_list()
    keys = list(coin_list.keys())
    
    for keyIndex in range(len(keys)):
        if not coin_list[keys[keyIndex]]['Rating']['Weiss']['Rating']:
            del coin_list[keys[keyIndex]]
            
    coin_list = pd.DataFrame().from_dict(coin_list, orient='index')
      
    return coin_list[['Name', 'CoinName', 'Rating']]
    
    
def loadExPair():
    ex_list = crt.get_exchanges()
    keys = list(ex_list.keys())
    
    for keyIndex in range(len(keys)):
        if ex_list[keys[keyIndex]]['Grade'] not in ['AA', 'A', 'BB', 'B']:
            del ex_list[keys[keyIndex]]
            
    
    exData = pd.DataFrame(columns=['exchange', 'fsym', 'tsym'])
                          
    keys = list(ex_list.keys())
    
    for key in keys:
        pairs = crt.get_pairs(exchange = key)
        
        for i in range(len(pairs)):
            exData = exData.append(pairs[i], ignore_index=True)
     
    return exData
        

    
def loadExchange():
    
    ex_list = crt.get_exchanges()
    keys = list(ex_list.keys())
    
    for keyIndex in range(len(keys)):
        if ex_list[keys[keyIndex]]['Grade'] not in ['AA', 'A', 'BB', 'B']:
            del ex_list[keys[keyIndex]]
            
    ex_list = pd.DataFrame().from_dict(ex_list, orient='index')
    
    return ex_list[['Name', 'GradePoints', 'Grade',  'Country', 'Description', 'AffiliateURL', 'LogoUrl']]
    
    
    
def insertPriceTable(pandaDB):
    
    query = """drop table if exists coins_price"""
    cursor.execute(query)
    
    #create coin price table
    query = """create table if not exists coins_price(symbol varchar(20), price_usd float(7), marketCap float(20), 24hour_volume float(10), supply float(10), imageUrl LONGTEXT)"""
    cursor.execute(query)
    
    for i in range(len(pandaDB)):
        query = """insert into coins_price values(%s, %s, %s, %s, %s, %s)"""
        row = pandaDB.iloc[i]
        val = (row['FROMSYMBOL'], float(row['PRICE']), float(row['MKTCAP']), float(row['VOLUME24HOURTO']), float(row['SUPPLY']), row['IMAGEURL'])
        cursor.execute(query, val)
    
    mydbs.commit()
    
    
def insertCoinTable(pandaDB):
    
    query = """drop table if exists coins"""
    cursor.execute(query)
    
    #create coin table
    query = """create table if not exists coins(coin_symbol varchar(20), coin_name LONGTEXT, rating varchar(20))"""
    cursor.execute(query)
    
    
    for i in range(len(pandaDB)):
        query = """insert into coins values(%s, %s, %s)"""
        row = pandaDB.iloc[i]
        rate = row['Rating']['Weiss']['Rating']
        val = (row['Name'], row['CoinName'], rate)
        cursor.execute(query, val)
        
    mydbs.commit()


def insertExPairTable(pandaDB):
    
    query = """drop table if exists pairs"""
    cursor.execute(query)
    
    #create coin table
    query = """create table if not exists pairs(exchange varchar(20), from_curr varchar(20), to_curr varchar(20))"""
    cursor.execute(query)
    
    
    for i in range(len(pandaDB)):
        query = """insert into pairs values(%s, %s, %s)"""
        row = pandaDB.iloc[i]
        val = (row['exchange'], row['fsym'], row['tsym'])
        cursor.execute(query, val)
        
    mydbs.commit()
 

def insertExchangeTable(pandaDB):
    
    query = """drop table if exists exchange"""
    cursor.execute(query)
    
    #create coin table
    query = """create table if not exists exchange(exchange varchar(20), grade_point float(20), grade varchar(20), country LONGTEXT, description LONGTEXT, web LONGTEXT, image LONGTEXT)"""
    cursor.execute(query)
    
    
    for i in range(len(pandaDB)):
        query = """insert into exchange values(%s, %s, %s, %s, %s, %s, %s)"""
        row = pandaDB.iloc[i]
        val = (row['Name'], row['GradePoints'], row['Grade'], row['Country'], row['Description'], row['AffiliateURL'], row['LogoUrl'])
        cursor.execute(query, val)
        
    mydbs.commit()


coinTable = loadCoinData()
insertCoinTable(coinTable)    
print("Finish1")

priceTable = loadPriceData()
insertPriceTable(priceTable)
print("Finish2")

pairTable = loadExPair()
insertExPairTable(pairTable)
print("Finish3")

exchangeTable = loadExchange()
insertExchangeTable(exchangeTable)
print("Finish4")

