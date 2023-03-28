"""Fetch company information."""
import argparse
import json
import os
import requests
import time
import pathlib

from typing import List


def fetch_weekly_company_prices(key: str, tickers: List[str], fetch_limit):

    # Get list of companies we already have.
    companies_already_have = [os.path.splitext(c)[0] for c in os.listdir("weekly")]

    tickers_to_fetch = set(tickers) - set(companies_already_have)
    tickers_to_fetch = list(set(tickers) - set(companies_already_have))
    tickers_to_fetch.sort()
    tickers_to_fetch = tickers_to_fetch[:fetch_limit]
    for i, ticker in enumerate(tickers_to_fetch):
        print(f"{i}. {ticker}")
    print(
        f"Companies total: {len(tickers)}, already have: {len(companies_already_have)}, fetching: {len(tickers_to_fetch)}"
    )

    # Fetch weekly prices for each company
    for ticker in tickers_to_fetch:
        print(ticker)
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticker}&apikey={key}"
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        with open(f"weekly/{ticker}.json", "w") as f:
            f.write(r.text)
        time.sleep(12)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="fetch-company-info", description="Fetch company weekly stock price data"
    )
    parser.add_argument(
        "--tickers_filename",
        type=str,
        default="indexes.txt",
        help="text file of tickers to fetch",
    )
    parser.add_argument(
        "--fetchlimit",
        type=int,
        nargs="?",
        default=500,
        help="number of companies to fetch",
    )

    args = parser.parse_args()
    print(args)

    with open("config.json", "r") as f:
        key = json.load(f)["alphavantage-api-key"]

    # Get list of tickers.
    with open(args.tickers_filename, "r") as f:
        tickers = f.read().splitlines()

    pathlib.Path(".").mkdir(exist_ok=True)
    fetch_weekly_company_prices(key, tickers, args.fetchlimit)
