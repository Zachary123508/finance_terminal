import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from utils.helpers import print_table, log_action

def handle_commodity(symbol, action):
    ticker = yf.Ticker(symbol)
    if action == "summary":
        info = ticker.info
        data = {
            "Name": info.get("shortName", "N/A"),
            "Currency": info.get("currency", "N/A"),
            "Previous Close": info.get("previousClose", "N/A"),
            "Current Price": info.get("regularMarketPrice", "N/A"),
        }
        print_table(f"{symbol} Commodity Summary", data)
        log_action(f"commodities {symbol} summary", data)
    elif action == "chart":
        hist = ticker.history(period="1y")
        hist["Close"].plot(title=f"{symbol} 1-Year Price Trend")
        plt.show()
        log_action(f"commodities {symbol} chart", "Displayed 1Y chart")
    elif action == "metrics":
        hist = ticker.history(period="1y")
        prices = hist["Close"].dropna()
        if len(prices) < 2:
            print("Not enough data to compute metrics")
            return
        ret = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
        daily = prices.pct_change().dropna()
        vol = daily.std() * np.sqrt(252) * 100
        sharpe = (daily.mean() * 252) / (daily.std() * np.sqrt(252)) if daily.std() != 0 else np.nan
        downside = daily[daily < 0]
        sortino = (daily.mean() * 252) / (downside.std() * np.sqrt(252)) if len(downside) > 0 and downside.std() != 0 else np.nan
        # compute correlation with S&P 500 index (^GSPC)
        spy = yf.download("^GSPC", period="1y")["Close"].dropna()
        aligned_daily, aligned_spy = daily.align(spy.pct_change().dropna(), join='inner')
        corr = aligned_daily.corr(aligned_spy)
        metrics = {
            "1-Year Return (%)": round(float(ret), 2),
            "Volatility (%)": round(float(vol), 2),
            "Sharpe Ratio": round(float(sharpe), 2) if not np.isnan(sharpe) else "N/A",
            "Sortino Ratio": round(float(sortino), 2) if not np.isnan(sortino) else "N/A",
            "Correlation vs S&P 500": round(float(corr), 2) if not np.isnan(corr) else "N/A",
        }
        print_table(f"{symbol} Commodity Metrics", metrics)
        log_action(f"commodities {symbol} metrics", metrics)
    else:
        print("Invalid action. Use summary, chart, or metrics.")
