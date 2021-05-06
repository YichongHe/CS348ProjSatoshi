import numpy as np
from mysql.connector import connect, Error

mydbs = connect(
    host="localhost",
    user="he463",
    password="85719712")

cursor = mydbs.cursor()
cursor.execute("use satoshi")


def frontHTML(templatePath):
    fronthtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Satoshi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body>
    <div style="background-color: tomato;color: white;border: 2px solid black;margin: 20px;padding: 20px;">
      <h2><a href="/coin">Coin List</a></h2>
    </div>
    
    <div style="background-color: tomato;color: white;border: 2px solid black;margin: 20px;padding: 20px;">
      <h2><a href="/exchange">Exchange List</a></h2>
    </div>
    
  </body>
</html>"""
    path = templatePath + "\\frontPage.html"
    f = open(path, "w")
    f.write(fronthtml)
    f.close()
    
    
def coinHTMLS(templatePath):
    query = """select coins.coin_symbol, price_usd, marketCap, imageUrl, 24hour_volume, supply, num_exchange, coins.coin_name
    from coins 
    left join coins_price
    on coins.coin_symbol = coins_price.symbol
    left join (select from_curr, count(distinct(exchange)) as num_exchange from pairs group by from_curr) as numExchange
    on coins.coin_symbol = numExchange.from_curr"""
    cursor.execute(query)
    
    for row in cursor:
        path =  templatePath
        coinhtml = "<!DOCTYPE html>\n<html>"
        coin = row[0]
        price = row[1]
        marketCap = row[2]
        if price is None:
            continue
        image = "https://www.cryptocompare.com" + row[3]
        dayhour_volume = row[4]
        supply = row[5]
        num_ex = row[6]
        if num_ex is None:
            num_ex = 0
        fullname = row[7]
        
        coinhtml = coinhtml + '\n<head>\n<title>' + coin + '</title>\n</head>'
        coinhtml = coinhtml + '\n<body>'
        coinhtml = coinhtml + '\n<h1>' + fullname + ': ' + coin + '</h1>'
        
        backLink = "http://localhost:5000/coin"
        coinhtml = coinhtml + "<a href=" + backLink + ">" + "Go back</a>" 
        
        coinhtml = coinhtml + '\n<img src=' + image + '>'
        coinhtml = coinhtml + '\n<p>Price: ' + str(price) + '</p>'
        coinhtml = coinhtml + '\n<p>marketCap: ' + str(marketCap) + '</p>'
        coinhtml = coinhtml + '\n<p>24hour_volume: ' + str(dayhour_volume) + '</p>'
        coinhtml = coinhtml + '\n<p>total supply: ' + str(supply) + '</p>'
        coinhtml = coinhtml + '\n<p>number of exchanges can trade this coin: ' + str(num_ex) + '</p>'
        coinhtml = coinhtml + '\n</body>'
        coinhtml = coinhtml + '\n</html>'
        
        path = path + "\\" + coin + ".html"
        f = open(path, "w")
        f.write(coinhtml)
        f.close()
        
        
def frontCoinHTML(templatePath):
    query = """select coins.coin_symbol, price_usd, marketCap, rating
    from coins 
    left join coins_price
    on coins.coin_symbol = coins_price.symbol
    order by marketCap desc"""
    cursor.execute(query)
    
    coinhtml = coinhtml = "<!DOCTYPE html>\n<html>"
    coinhtml = coinhtml + '\n<head>\n<title>coin</title>\n</head>'
    coinhtml = coinhtml + '\n<body>'
    coinhtml = coinhtml + '\n<h1>Coins</h1>'
    backLink = "http://localhost:5000/"
    coinhtml = coinhtml + "<a href=" + backLink + ">" + "Go back</a>" 
    coinhtml = coinhtml + "\n<table border = '1'>"
    coinhtml = coinhtml + '\n<tr>'
    coinhtml = coinhtml + '\n<th>Coin</th>'
    coinhtml = coinhtml + '\n<th>price(USD)</th>'
    coinhtml = coinhtml + '\n<th>marketCap(USD)</th>'
    coinhtml = coinhtml + '\n<th>Weiss Rating</th>'
    coinhtml = coinhtml + '\n</tr>'
    for row in cursor:
        coinhtml = coinhtml + '\n<tr>'
        link = "http://localhost:5000/coin/" + row[0]
        coinhtml = coinhtml + "\n<td><a href=" + link + ">" + row[0] + '</a></td>'
        coinhtml = coinhtml + "\n<td>" + str(row[1]) + "</td>"
        coinhtml = coinhtml + "\n<td>" + str(row[2]) + "</td>"
        coinhtml = coinhtml + "\n<td>" + row[3] + "</td>"
        coinhtml = coinhtml + '\n</tr>'
        
    path = templatePath + "\\coins.html"
    f = open(path, "w")
    f.write(coinhtml)
    f.close()
    
    
def exchangeHTMLS(templatePath):
    query = """select e.exchange, count(distinct(p.from_curr)) as "number of currencies", grade_point, country, web, image, description, from_curr
    from exchange e
    left join pairs p
    on e.exchange = p. exchange
    group by e.exchange"""
    cursor.execute(query)
    
    for row in cursor:
        path =  templatePath
        coinhtml = "<!DOCTYPE html>\n<html>"
        image = "https://www.cryptocompare.com" + row[5]

        coinhtml = coinhtml + '\n<head>\n<title>exchange</title>\n</head>'
        coinhtml = coinhtml + '\n<body>'
        coinhtml = coinhtml + '\n<h1>' + row[0] + '</h1>'
        
        backLink = "http://localhost:5000/exchange"
        coinhtml = coinhtml + "<a href=" + backLink + ">" + "Go back</a>" 
        
        coinhtml = coinhtml + '\n<img src=' + image + '>'
        coinhtml = coinhtml + '\n<p>grade pointe: ' + str(row[2]) + '</p>'
        coinhtml = coinhtml + '\n<p>country: ' + str(row[3]) + '</p>'
        coinhtml = coinhtml + '\n<p>number of currencies: ' + str(row[1]) + '</p>'
        coinhtml = coinhtml + '\n<p>website link: <a href=' + "'" + str(row[4]) + "'>" + row[0] + '</a></p>'
        coinhtml = coinhtml + '\n<p>detailed description: ' + str(row[6]) + '</p>'
        coinhtml = coinhtml + '\n<p>pair table: <a href=' + "'http://localhost:5000/exchange/" + row[0] + "/table'>table</a></p>"
        
        
        coinhtml = coinhtml + '\n</body>'
        coinhtml = coinhtml + '\n</html>'

        path = path + "\\" + row[0] + ".html"
        f = open(path, "w", encoding='utf-8')
        f.write(coinhtml)
        f.close()
    
    
def frontExchangeHTML(templatePath):
    query = """select *
    from exchange
    order by grade_point desc"""
    cursor.execute(query)
    
    coinhtml = coinhtml = "<!DOCTYPE html>\n<html>"
    coinhtml = coinhtml + '\n<head>\n<title>exchange</title>\n</head>'
    coinhtml = coinhtml + '\n<body>'
    coinhtml = coinhtml + '\n<h1>Exchange</h1>'
    backLink = "http://localhost:5000/"
    coinhtml = coinhtml + "<a href=" + backLink + ">" + "Go back</a>" 
    coinhtml = coinhtml + "\n<table border = '1'>"
    coinhtml = coinhtml + '\n<tr>'
    coinhtml = coinhtml + '\n<th>Name</th>'
    coinhtml = coinhtml + '\n<th>grade(USD)</th>'
    coinhtml = coinhtml + '\n<th>country</th>'
    coinhtml = coinhtml + '\n</tr>'
    for row in cursor:
        coinhtml = coinhtml + '\n<tr>'
        link = "http://localhost:5000/exchange/" + row[0]
        coinhtml = coinhtml + "\n<td><a href=" + link + ">" + row[0] + '</a></td>'
        coinhtml = coinhtml + "\n<td>" + str(row[2]) + "</td>"
        coinhtml = coinhtml + "\n<td>" + str(row[3]) + "</td>"
        coinhtml = coinhtml + '\n</tr>'
        
    path = templatePath + "\\exchanges.html"
    f = open(path, "w")
    f.write(coinhtml)
    f.close()


def pairHTMLS(templatePath):
    query = "DROP PROCEDURE IF EXISTS selectAllPairs;"
    cursor.execute(query)
    
    query = """
    CREATE PROCEDURE selectAllPairs (IN exName varchar(30))
    BEGIN
    	select * from pairs where exchange = exName;
    END
    """
    cursor.execute(query)
    
    exchangeList = []
    cursor.execute("""select exchange from exchange""")
    for i in cursor:
        exchangeList.append(i[0])
        
    for k in exchangeList:
        cursor.callproc("selectAllPairs", [k,])
        for row in cursor.stored_results():
            pairs = row.fetchall()
            
            pairhtml = "<!DOCTYPE html>\n<html>"
            backLink = "http://localhost:5000/exchange/" + k 
            pairhtml = pairhtml + "<body>"
            pairhtml = pairhtml + "\n<p><a href=" + backLink + ">" + "Go back</a></p>" 
            pairhtml = pairhtml + "\n<table border = '1'>"
            pairhtml = pairhtml + '\n<tr>'
            pairhtml = pairhtml + '\n<th>from</th>'
            pairhtml = pairhtml + '\n<th>to</th>'
            pairhtml = pairhtml + '\n</tr>'
            
            if len(pairs) > 0:
                for pair in pairs:
                    pairhtml = pairhtml + '\n<tr>'
                    pairhtml = pairhtml + "\n<td>" + pair[1] + "</td>"
                    pairhtml = pairhtml + "\n<td>" + pair[2] + "</td>"
                    pairhtml = pairhtml + '\n</tr>'
                    
            pairhtml = pairhtml + '</table></body></html>'
            path = templatePath + "\\" + k + "table.html"
            f = open(path, "w")
            f.write(pairhtml)
            f.close()   


def run(filePath):
    
    frontHTML(filePath)
    
    coinHTMLS(filePath)
    frontCoinHTML(filePath)
    
    exchangeHTMLS(filePath)
    frontExchangeHTML(filePath)
    
    pairHTMLS(filePath)


run("C:\\Users\\JimHentai\\FlaskApp\\templates")

