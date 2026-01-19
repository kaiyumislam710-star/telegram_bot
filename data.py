from binance.client import Client
import pandas as pd

API_KEY = "ZUKLAT5zh16MkfRUA67DZTZB6fyBMhVx7jMRKnFWBeOhbKuHe2AGJFYN0LjXuXVz"
API_SECRET = "0BeIWjtbpgKETQbW24FrBZjgKE5pPnl7WclYlyf5j4rcQJsIKKYKAQkkBN25veWE"

client = Client(API_KEY, API_SECRET)

def get_candles(symbol="EURUSDT", interval="1m", limit=50):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'c1','c2','c3','c4','c5','c6'
    ])
    df['close'] = df['close'].astype(float)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    return df