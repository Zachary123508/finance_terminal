import yfinance as yf
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
    hist = ticker.history(period="6mo")
    returns = hist["Close"].pct_change().dropna()
    result = {
        "6-Month Return (%)": round((hist["Close"][-1]/hist["Close"][0] - 1) * 100, 2),
        "Volatility (%)": round(returns.std() * 100, 2)
    }
    print_table(f"{ticker.ticker} Metrics", result)
    log_action(f"stocks {ticker.ticker} metrics", result)
