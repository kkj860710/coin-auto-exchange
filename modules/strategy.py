import pandas as pd
import time
from upbit_api import get_ticker, buy_coin, sell_coin

def calculate_macd(df):
    df["EMA12"] = df["trade_price"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["trade_price"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    return df

def auto_trade(market="KRW-BTC"):
    while True:
        price = get_ticker(market)
        df = pd.DataFrame([{"trade_price": price}])  # 실시간 데이터
        df = calculate_macd(df)

        macd = df["MACD"].iloc[-1]
        signal = df["Signal"].iloc[-1]

        if macd > signal:
            print("📈 매수")
            buy_coin(market, 10000)
        elif macd < signal:
            print("📉 매도")
            sell_coin(market, 0.001)

        time.sleep(60)  # 1분마다 실행
