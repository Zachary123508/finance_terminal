import yfinance as yf
import matplotlib.pyplot as plt
from utils.helpers import print_table, log_action


def handle_compare(symbols, action):
    # Accept comma-separated symbols string or list
    if isinstance(symbols, str):
        symbols = [s.strip() for s in symbols.split(",")]
    # Download closing prices for the symbols over 1 year
    data = yf.download(symbols, period="1y")["Close"]
    if action == "chart":
        # Normalize prices to 100 at start to compare growth
        normalized = data / data.iloc[0] * 100
        normalized.plot(title="Comparison Chart")
        plt.xlabel("Date")
        plt.ylabel("Normalized Price (start=100)")
        plt.legend(symbols)
        plt.show()
        log_action(f"compare {'-'.join(symbols)} chart", "Displayed comparison chart")
    elif action == "metrics":
        metrics = {}
        for sym in symbols:
            series = data[sym]
            # compute 1-year return and volatility
            ret = (series.iloc[-1] / series.iloc[0] - 1) * 100
            vol = series.pct_change().dropna().std() * 100
            metrics[sym] = {
                "1-Year Return (%)": round(ret, 2),
                "Volatility (%)": round(vol, 2)
            }
        print_table("Comparison Metrics", metrics)
        log_action(f"compare {'-'.join(symbols)} metrics", metrics)
    else:
        print("Comparison supports chart and metrics.")
