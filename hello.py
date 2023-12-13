from flask import Flask, render_template, request, url_for
from datetime import datetime, timedelta
import requests
import json
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import time
import matplotlib
matplotlib.use('agg')  # Set the backend to 'agg'
from matplotlib import pyplot as plt
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)

engine = create_engine('sqlite:///currency.db')
#Session = sessionmaker(bind=engine)
#session = Session()


@app.route('/')
def index():
    # Retrieve the latest data from the database
    return render_template('index.html')



@app.route('/fetch-USD', methods=['POST'])
def fetch_USD():
    conn = sqlite3.connect('currency.db')
    cur = conn.cursor()
    cur.execute("SELECT EUR, GBP, INR, JPY, CHF, AUD, NZD FROM currencyData WHERE base='USD'")
    usd_data = cur.fetchall()    
    x = ['EUR', 'GBP', 'INR', 'JPY', 'CHF', 'AUD', 'NZD']
    y = usd_data[0]
    plt.clf()
    plt.plot(x, y , marker='o', label='Exchange Rate')
    plt.ylabel('Amount')
    plt.xlabel('Currency')
    plt.title('USD Exchange Rates for Today')
    for i in range(len(x)):
        plt.text(x[i], y[i]+0.1, y[i], ha='center')
    plt.legend()

    img_filename = 'USD_graph.png'
    img_path_usd = url_for('static', filename=img_filename)
    plt.savefig(f"static/{img_filename}")  # Save the image in the 'static' folder

    ans_usd = "USD Data Displayed success"
    return render_template('index.html', ans=ans_usd, data_usd=usd_data[0], img_path_usd=img_path_usd)


@app.route('/fetch-CAD', methods=['POST'])
def fetch_CAD():
    conn = sqlite3.connect('currency.db')
    cur = conn.cursor()
    cur.execute("SELECT EUR, GBP, INR, JPY, CHF, AUD, NZD FROM currencyData WHERE base='CAD'")
    cad_data = cur.fetchall()
    print(cad_data)
    x = ['EUR', 'GBP', 'INR', 'JPY', 'CHF', 'AUD', 'NZD']
    y = cad_data[0]
    plt.clf()
    plt.plot(x, y , marker='o', label='Exchange Rate')
    plt.ylabel('Amount')
    plt.xlabel('Currency')
    plt.title('CAD Exchange Rates for Today')
    for i in range(len(x)):
        plt.text(x[i], y[i]+0.1, y[i], ha='center')
    plt.legend()

    img_filename = 'CAD_graph.png'
    img_path_cad = url_for('static', filename=img_filename)
    plt.savefig(f"static/{img_filename}")  # Save the image in the 'static' folder

    ans_cad = "CAD Data Displayed success"
    return render_template('index.html', ans=ans_cad, data_cad=cad_data[0], img_path_cad=img_path_cad)



@app.route('/update-data', methods=['POST'])
def update_data():
    # Make the API request and get the data
    conn = sqlite3.connect('currency.db')
    cur = conn.cursor()
    #cur.execute("DROP TABLE currencyData")
    #cur.execute("CREATE TABLE currencyData (ymd timestamp, base string, EUR float, GBP float, INR float, JPY float, CHF float, AUD float, NZD float )")
    cur.execute("DELETE FROM currencyData")
    print("Step 1 - Update")
    data_UpdateDate = ""
    url = "https://api.exchangerate-api.com/v4/latest/"
    baseCurrency = ["CAD","USD"]
    today = datetime.now()
    print("Step 2 - Update")
    print(str(today)!=str(data_UpdateDate))
    if(str(today)!=str(data_UpdateDate)):
        for i in baseCurrency:    
            response = requests.get(url+i)
            data = json.loads(response.text)
            print("Step 3 - Update")
            # Get the data from the past year and store it in the database
            curData = data["rates"]
            val_tuple = (today, i, curData['EUR'], curData['GBP'], curData['INR'], curData['JPY'], curData['CHF'], curData['AUD'], curData['NZD'])
            cur.execute("INSERT INTO currencyData VALUES (?,?,?,?,?,?,?,?,?)", val_tuple);
        data_UpdateDate = str(today)
    print(data_UpdateDate)
    conn.commit()
    cur.close()
    conn.close()
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)



