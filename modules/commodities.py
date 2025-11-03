import yfinance as yf
import matplotlib.pyplot as plt
from utils.helpers import print_table, log_action


def handle_commodity(symbol, action):
    ticker = yf.Ticker(symbol)
    if action == "summary":
        info = ticker.info
        data = {
            "Name": info.get("shortName", "N/A"),
            "Currency": info.get("currency", "N/A"),
            "Previous Close": info.get("previousClose", "N/A")
        }
        print_table(f"{symbol} Commodity Summary", data)
        log_action(f"commodities {symbol} summary", data)
    elif action == "chart":
        hist = ticker.history(period="1y")
        hist["Close"].plot(title=f"{symbol} 1-Year Price Trend")
        plt.show()
        log_action(f"commodities {symbol} chart", "Displayed 1Y chart")
    elif action == "metrics":
        hist = ticker.history(period="6mo")
        change = (hist["Close"][-1]/hist["Close"][0] - 1) * 100
        print_table(f"{symbol} Commodity Metrics", {"6-Month Change (%)": round(change, 2)})
        log_action(f"commodities {symbol} metrics", f"{round(change, 2)}%")
