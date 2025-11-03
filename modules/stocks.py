import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from utils.helpers import print_table, log_action


def handle_stock(symbol, action):
    ticker = yf.Ticker(symbol)
    if action == "summary":
        show_summary(ticker)
    elif action == "chart":
        show_chart(ticker)
    elif action == "metrics":
        show_metrics(ticker)


def show_summary(ticker):
    info = ticker.info
    data = {
        "Name": info.get("shortName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "Return on Assets": info.get("returnOnAssets", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A")
    }
    print_table(f"{info.get('symbol', 'Unknown')} Summary", data)
    log_action(f"stocks {info.get('symbol')} summary", data)


def show_chart(ticker):
    hist = ticker.history(period="1y")
    hist["Close"].plot(title=f"{ticker.ticker} 1-Year Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.show()
    log_action(f"stocks {ticker.ticker} chart", "Displayed 1Y price chart")


def show_metrics(ticker):
    hist = ticker.history(period="1y")
    prices = hist["Close"]
    returns = prices.pct_change().dropna()
    total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
    vol = returns.std() * np.sqrt(252) * 100
    sharpe = (returns.mean() * 252) / (returns.std() * np.sqrt(252))
    downside_returns = returns[returns < 0]
    if len(downside_returns) > 0:
        downside_std = downside_returns.std() * np.sqrt(252)
        sortino = (returns.mean() * 252) / downside_std if downside_std != 0 else np.nan
    else:
        sortino = np.nan
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdowns = (cumulative - running_max) / running_max
    max_drawdown = drawdowns.min() * 100
    result = {
        "1-Year Return (%)": round(float(total_return), 2),
        "Annualized Volatility (%)": round(float(vol), 2),
        "Sharpe Ratio": round(float(sharpe), 2) if not np.isnan(sharpe) else "N/A",
        "Sortino Ratio": round(float(sortino), 2) if not np.isnan(sortino) else "N/A",
        "Max Drawdown (%)": round(float(max_drawdown), 2)
    }
    print_table(f"{ticker.ticker} Advanced Metrics", result)
    log_action(f"stocks {ticker.ticker} metrics", result)
