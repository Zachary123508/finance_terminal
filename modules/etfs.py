import yfinance as yf
import matplotlib.pyplot as plt
from utils.helpers import print_table, log_action


def handle_etf(symbol, action):
    if action == "summary":
        data = yf.Ticker(symbol)
        info = data.info
        details = {
            "Name": info.get("shortName", "N/A"),
            "Category": info.get("category", "N/A"),
            "Expense Ratio": info.get("annualReportExpenseRatio", "N/A"),
            "Holdings Count": info.get("totalAssets", "N/A")
        }
        print_table(f"{symbol} ETF Summary", details)
        log_action(f"etf {symbol} summary", details)
    elif action == "chart":
        data = yf.download(symbol, period="1y")
        # Plot closing price
        data["Close"].plot(title=f"{symbol} ETF Price Chart")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.show()
        log_action(f"etf {symbol} chart", "Displayed price chart")
    elif action == "metrics":
        data = yf.download(symbol, period="6mo")
        change = (data["Close"][-1] / data["Close"][0] - 1) * 100
        print_table(f"{symbol} ETF Metrics", {"6-Month Change (%)": round(change, 2)})
        log_action(f"etf {symbol} metrics", f"{round(change, 2)}%")
    else:
        print("ETFs currently support summary, chart and metrics only.")
