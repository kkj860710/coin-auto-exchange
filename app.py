from flask import Flask, render_template, jsonify
from modules.upbit_api import get_balance, get_ticker
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/balance')
def balance():
    return jsonify(get_balance())

@app.route('/price')
def price():
    btc_price = get_ticker("KRW-BTC")
    return jsonify({"btc_price": btc_price})

@app.route('/chart')
def chart():
    df = pd.DataFrame([{"time": "2025-02-14", "price": get_ticker("KRW-BTC")}])
    fig = go.Figure(data=[go.Scatter(x=df["time"], y=df["price"], mode="lines")])
    graph = fig.to_html(full_html=False)
    return render_template('chart.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
