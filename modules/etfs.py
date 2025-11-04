import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from utils.helpers import print_table, log_action

def handle_etf(symbol, action):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    if action == "summary":
        details = {
            "Name": info.get("shortName", "N/A"),
            "Category": info.get("category", "N/A"),
            "Expense Ratio": info.get("annualReportExpenseRatio", "N/A"),
            "Assets Under Management": info.get("totalAssets", "N/A"),
            "Average Volume": info.get("averageVolume", "N/A"),
            "Dividend Yield": info.get("yield", "N/A"),
            "Fund Family": info.get("fundFamily", "N/A"),
            "Inception Date": info.get("fundInceptionDate", "N/A"),
            "Total Holdings": info.get("holdingsCount", "N/A"),
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
        hist = ticker.history(period="5y")
        prices = hist["Close"].dropna()
        if len(prices) < 2:
            print("Not enough data to compute metrics")
            return
        def calc_return(years):
            period_days = int(252 * years)
            if len(prices) < period_days:
                return np.nan
            start = prices.iloc[-period_days]
            end = prices.iloc[-1]
            return (end / start - 1) * 100
        returns = {
            "1-Year Return (%)": calc_return(1),
            "3-Year Return (%)": calc_return(3),
            "5-Year Return (%)": calc_return(5),
        }
        total_years = (prices.index[-1] - prices.index[0]).days / 365.25
        cagr = ((prices.iloc[-1] / prices.iloc[0]) ** (1 / total_years) - 1) * 100 if total_years > 0 else np.nan
        daily = prices.pct_change().dropna()
        vol = daily.std() * np.sqrt(252) * 100
        sharpe = (daily.mean() * 252) / (daily.std() * np.sqrt(252)) if daily.std() != 0 else np.nan
        downside = daily[daily < 0]
        sortino = (daily.mean() * 252) / (downside.std() * np.sqrt(252)) if len(downside) > 0 and downside.std() != 0 else np.nan
        cum = (1 + daily).cumprod()
        peak = cum.cummax()
        drawdown = (cum - peak) / peak
        max_drawdown = drawdown.min() * 100
        metrics = {
            "1-Year Return (%)": round(float(returns["1-Year Return (%)"]), 2) if not np.isnan(returns["1-Year Return (%)"]) else "N/A",
            "3-Year Return (%)": round(float(returns["3-Year Return (%)"]), 2) if not np.isnan(returns["3-Year Return (%)"]) else "N/A",
            "5-Year Return (%)": round(float(returns["5-Year Return (%)"]), 2) if not np.isnan(returns["5-Year Return (%)"]) else "N/A",
            "CAGR (%)": round(float(cagr), 2) if not np.isnan(cagr) else "N/A",
            "Volatility (%)": round(float(vol), 2) if not np.isnan(vol) else "N/A",
            "Sharpe Ratio": round(float(sharpe), 2) if not np.isnan(sharpe) else "N/A",
            "Sortino Ratio": round(float(sortino), 2) if not np.isnan(sortino) else "N/A",
            "Max Drawdown (%)": round(float(max_drawdown), 2) if not np.isnan(max_drawdown) else "N/A",
        }
        print_table(f"{symbol} ETF Metrics", metrics)
        log_action(f"etf {symbol} metrics", metrics)
    else:
        print("Invalid action. Use summary, chart, or metrics.")
