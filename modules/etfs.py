import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from utils.helpers import print_table, log_action


def handle_etf(symbol, action):
    ticker = yf.Ticker(symbol)
    if action == "summary":
        info = ticker.info
        details = {
            "Name": info.get("shortName", "N/A"),
            "Category": info.get("category", "N/A"),
            "Expense Ratio": info.get("annualReportExpenseRatio", "N/A"),
            "Assets Under Management": info.get("totalAssets", "N/A"),
            "Average Volume": info.get("averageVolume", "N/A"),
        }
        print_table(f"{symbol} ETF Summary", details)
        log_action(f"etf {symbol} summary", details)
    elif action == "chart":
        hist = ticker.history(period="1y")
        hist["Close"].plot(title=f"{symbol} 1-Year Price Trend")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.show()
        log_action(f"etf {symbol} chart", "Displayed 1Y price chart")
    elif action == "metrics":
        hist = ticker.history(period="1y")
        prices = hist["Close"]
        returns = prices.pct_change().dropna()
        total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
        vol = returns.std() * np.sqrt(252) * 100
        sharpe = (returns.mean() * 252) / (returns.std() * np.sqrt(252))
        downside = returns[returns < 0]
        if len(downside) > 0:
            downside_std = downside.std() * np.sqrt(252)
            sortino = (returns.mean() * 252) / downside_std if downside_std != 0 else np.nan
        else:
            sortino = np.nan
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.cummax()
        drawdowns = (cumulative - running_max) / running_max
        max_drawdown = drawdowns.min() * 100
        metrics = {
            "1-Year Return (%)": round(float(total_return), 2),
            "Annualized Volatility (%)": round(float(vol), 2),
            "Sharpe Ratio": round(float(sharpe), 2) if not np.isnan(sharpe) else "N/A",
            "Sortino Ratio": round(float(sortino), 2) if not np.isnan(sortino) else "N/A",
            "Max Drawdown (%)": round(float(max_drawdown), 2),
        }
        print_table(f"{symbol} ETF Advanced Metrics", metrics)
        log_action(f"etf {symbol} metrics", metrics)
    else:
        print("ETFs currently support summary, chart and metrics only.")
