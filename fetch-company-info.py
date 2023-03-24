"""Fetch company information."""
import json
import os
import requests
import time

from typing import List


def fetch_weekly_company_prices(key: str, companies: List[str]):

    # Get list of companies we already have.
    companies_already_have = [os.path.splitext(c)[0] for c in os.listdir("weekly")]

    companies_to_fetch = set(companies) - set(companies_already_have)
    companies_to_fetch = list(set(companies) - set(companies_already_have))
    companies_to_fetch.sort()
    ALPHAVANTGE_MAX_QUERIES_PER_DAY = 500
    companies_to_fetch = companies_to_fetch[:ALPHAVANTGE_MAX_QUERIES_PER_DAY]
    for i, ticker in enumerate(companies_to_fetch):
        print(f"{i}. {ticker}")
    print(
        f"Companies total: {len(companies)}, already have: {len(companies_already_have)}, fetching: {len(companies_to_fetch)}"
    )

    # Fetch weekly prices for each company
    for company in companies_to_fetch:
        print(company)
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={company}&apikey={key}"
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        with open(f"weekly/{company}.json", "w") as f:
            f.write(r.text)
        time.sleep(12)


if __name__ == "__main__":

    with open("config.json", "r") as f:
        key = json.load(f)["alphavantage-api-key"]

    # Get list of sp500 companies.
    with open("healthcare-companies.txt", "r") as f:
        companies = f.read().splitlines()

    fetch_weekly_company_prices(key, companies)
