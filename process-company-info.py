import copy
import datetime
import json
import os
import sys
import pathlib
from typing import List


def week_dict_to_list(week_dict) -> List[float]:
    """Convert "yyyy-mm-dd" -> {} mapping to a flat list."""
    l = []
    for key, value in week_dict.items():
        week = copy.deepcopy(value)
        week["day"] = key
        l.append(week)
    l.sort(key=lambda x: x["day"], reverse=True)
    return l


def calculate_year_over_year(weeks: List[float]) -> List[float]:
    """Calculate year over year change from weekly adjusted close."""
    weekly_closes = [float(x["5. adjusted close"]) for x in weeks]
    year_over_year = []
    for i in range(len(weekly_closes) - 53):
        now = weekly_closes[i]
        last_year = weekly_closes[i + 52]
        year_over_year.append((now - last_year) / last_year)
    return year_over_year


class CompanyInfo:
    def __init__(self, ticker, year_over_year: list[float]):
        self.ticker = ticker
        self.weeks = year_over_year


def get_all_companies_info(tickers: List[str]) -> List[CompanyInfo]:
    all_companies_info = []
    for ticker in tickers:
        with open(f"weekly/{ticker}.json", "r") as f:
            j = json.load(f)
        try:
            weeks = week_dict_to_list(j["Weekly Adjusted Time Series"])
        except KeyError:
            print(f"KeyError: {ticker}")
            continue
        all_companies_info.append(CompanyInfo(ticker, weeks))
    return all_companies_info


def print_history_stats(all_companies_info):
    all_num_weeks = [len(ci.weeks) for ci in all_companies_info]
    all_num_weeks.sort()
    print(f"Total companies: {len(all_num_weeks)}")
    for i, num_weeks in enumerate(all_num_weeks):
        if num_weeks > 52:
            print(f"Num companies < 1 year of history: {i}")
            break
    print("Years of history:")
    print(f" - min: {all_num_weeks[0]/52.0}")
    print(f" - median: {all_num_weeks[len(all_num_weeks)//2]/52.0}")
    print(f" - max: {all_num_weeks[len(all_num_weeks) - 1]/52.0}")


if __name__ == "__main__":

    with open("healthcare-companies.txt", "r") as f:
        tickers = f.read().splitlines()
        all_companies_info = get_all_companies_info(tickers)
    print_history_stats(all_companies_info)

    # company_info = process_company_info("weekly/AADI.json")
    # print(f"ADDI: {company_info.years_of_history}")
