"""Fetch company information."""
import os
import requests
import time


def fetch_weekly_company_prices():

    # Get list of sp500 companies.
    with open("sp500-companies.txt", "r") as f:
        sp500_companies = f.read().splitlines()

    # Get list of companies we already have.
    companies_already_have = [os.path.splitext(c)[0] for c in os.listdir("weekly")]
    print(companies_already_have)

    companies_to_fetch = set(sp500_companies) - set(companies_already_have)
    companies_to_fetch = list(set(sp500_companies) - set(companies_already_have))
    companies_to_fetch.sort()
    print(companies_to_fetch)
    print(len(companies_to_fetch))

    key = "KEY HERE"
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


fetch_weekly_company_prices()
