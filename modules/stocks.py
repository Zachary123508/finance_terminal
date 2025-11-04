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
        "Forward P/E": info.get("forwardPE", "N/A"),
        "PEG Ratio": info.get("pegRatio", "N/A"),
        "P/B Ratio": info.get("priceToBook", "N/A"),
        "P/S Ratio": info.get("priceToSalesTrailing12Months", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
        "Payout Ratio": info.get("payoutRatio", "N/A"),
        "EPS": info.get("trailingEps", "N/A"),
        "Revenue Growth (YoY)": info.get("revenueGrowth", "N/A"),
        "Return on Equity": info.get("returnOnEquity", "N/A"),
        "Return on Assets": info.get("returnOnAssets", "N/A"),
        "Profit Margin": info.get("profitMargins", "N/A"),
        "Operating Margin": info.get("operatingMargins", "N/A"),
        "Beta": info.get("beta", "N/A"),
        "Short Ratio": info.get("shortRatio", "N/A")
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
    hist = ticker.history(period="5y")
    prices = hist["Close"]
    returns_daily = prices.pct_change().dropna()
    # compute total returns for 1, 3, 5 years using tail windows if available
    def compute_total_return(series):
        if len(series) < 2:
            return np.nan
        return (series.iloc[-1] / series.iloc[0] - 1) * 100
    one_year = prices.tail(252)
    three_year = prices.tail(252 * 3)
    five_year = prices
    total_return_1 = compute_total_return(one_year)
    total_return_3 = compute_total_return(three_year)
    total_return_5 = compute_total_return(five_year)
    # risk metrics
    annualized_vol = returns_daily.std() * np.sqrt(252) * 100
    sharpe = (returns_daily.mean() * 252) / (returns_daily.std() * np.sqrt(252))
    downside_returns = returns_daily[returns_daily < 0]
    if len(downside_returns) > 0:
        downside_std = downside_returns.std() * np.sqrt(252)
        sortino = (returns_daily.mean() * 252) / downside_std if downside_std != 0 else np.nan
    else:
        sortino = np.nan
    cumulative = (1 + returns_daily).cumprod()
    running_max = cumulative.cummax()
    drawdowns = (cumulative - running_max) / running_max
    max_drawdown = drawdowns.min() * 100 if len(drawdowns) > 0 else np.nan
    result = {
        "1-Year Return (%)": round(float(total_return_1), 2) if not np.isnan(total_return_1) else "N/A",
        "3-Year Return (%)": round(float(total_return_3), 2) if not np.isnan(total_return_3) else "N/A",
        "5-Year Return (%)": round(float(total_return_5), 2) if not np.isnan(total_return_5) else "N/A",
        "Annualized Volatility (%)": round(float(annualized_vol), 2) if not np.isnan(annualized_vol) else "N/A",
        "Sharpe Ratio": round(float(sharpe), 2) if not np.isnan(sharpe) else "N/A",
        "Sortino Ratio": round(float(sortino), 2) if not np.isnan(sortino) else "N/A",
        "Max Drawdown (%)": round(float(max_drawdown), 2) if not np.isnan(max_drawdown) else "N/A"
    }
    print_table(f"{ticker.ticker} Performance Metrics", result)
    log_action(f"stocks {ticker.ticker} metrics", result)
