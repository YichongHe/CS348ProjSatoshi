import numpy as np
from flask import Flask, render_template
from mysql.connector import connect, Error

mydbs = connect(
    host="localhost",
    user="he463",
    password="85719712")

app = Flask(__name__)
cursor = mydbs.cursor()
cursor.execute("use satoshi")




@app.route('/')
def frontPage():
    return render_template("frontPage.html")



    
@app.route('/coin/<coinname>')
def coinsPages(coinname):
    return render_template(coinname + ".html")




@app.route('/coin')
def coinPage():
    
    return render_template("coins.html")




    
@app.route('/exchange/<exchangename>')
def exchangessPages(exchangename):
    return render_template(exchangename + ".html")





@app.route('/exchange')
def exchangePage():
    return render_template("exchanges.html")




        
@app.route('/exchange/<exchange>/table')
def pairPages(exchange):
    return render_template(exchange + "table.html")



if __name__ == '__main__':
    app.run(debug=False)