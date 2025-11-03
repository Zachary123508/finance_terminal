import argparse
from modules import stocks, etfs, commodities, compare


def main():
    parser = argparse.ArgumentParser(description="Finance Terminal CLI")
    parser.add_argument("module", choices=["stocks", "etfs", "commodities", "compare"], help="Choose a module")
    parser.add_argument("symbol", help="Ticker or symbol (e.g. AAPL, SPY, GOLD) or comma-separated list for compare")
    parser.add_argument("action", choices=["summary", "chart", "metrics"], help="Action to perform")
    args = parser.parse_args()

    if args.module == "stocks":
        stocks.handle_stock(args.symbol, args.action)
    elif args.module == "etfs":
        etfs.handle_etf(args.symbol, args.action)
    elif args.module == "commodities":
        commodities.handle_commodity(args.symbol, args.action)
    elif args.module == "compare":
        compare.handle_compare(args.symbol, args.action)


if __name__ == "__main__":
    main()
