import os, time
import pandas as pd
import yfinance as yf

TICKERS = ["VOO", "QQQ", "AAPL", "MSFT", "HLAL", "SPY"]
START = "1999-01-01"
OUT = "data"
os.makedirs(OUT, exist_ok=True)

def from_yahoo(t):
    df = yf.download(t, start=START, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError("kosong")
    s = df["Close"].squeeze().rename("adj_close")
    return s.to_frame()

def from_stooq(t):  # cadangan kalau Yahoo menolak
    url = f"https://stooq.com/q/d/l/?s={t.lower()}.us&i=d"
    df = pd.read_csv(url, parse_dates=["Date"], index_col="Date")
    return df[["Close"]].rename(columns={"Close": "adj_close"})

for t in TICKERS:
    for src in (from_yahoo, from_stooq):
        try:
            df = src(t)
            df.index.name = "date"
            df.round(4).to_csv(f"{OUT}/{t}.csv")
            print(f"{t}: {len(df)} baris via {src.__name__}, s.d. {df.index[-1].date()}")
            break
        except Exception as e:
            print(f"{t}: {src.__name__} gagal ({e})")
            time.sleep(2)
