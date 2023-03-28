# The Dude Compounds

New information has come to light. Allows dude to make better investment decisions.

So far this library:
1. Calculates the amount of weekly historical data provided by <https://www.alphavantage.co> for companies of interest.
2. Sees how many of these companies beat a given index.

The first cut of this looked at all publicly traded companies in the healthcare sector on March 28, 2023. Note because of the 500 API call limit it took 3 days to get information on all the companies:

    Total companies: 1291
    Num companies < 1 year of history: 49
    Years of history:
    - min: 0.057692307692307696
    - median: 5.8076923076923075
    - max: 23.5
    Year over year stats vs VTI (Vanguard Total Market Index):
    - Last week: beats: 324, total: 1241, percent: 26.10797743755036
    - Last year (weekly): beats: 12641, total: 60797, percent: 20.79214434922776
    - Last 3 years (weekly): beats: 45767, total: 154150, percent: 29.689912422964643
    - Last 5 years (weekly): beats: 71312, total: 228214, percent: 31.24786384709089

## Instructions

1. Clone/get this repo.
2. Get a key from <https://www.alphavantage.co/support/#api-key>
3. Create a config.json file at root level of repo:

    {
        "alphavantage-api-key": "KEYHERE"
    }

4. Download the stocks you are interested in getting from https://www.nasdaq.com/market-activity/stocks/screener as CSV file. Save only the column of ticker names. Save as a txt file like "tickers.csv"
5. Run fetch-company-info.py. Note there is a limit of [5 API requests per minute and 500 requests per day](https://www.alphavantage.co/support/#support).

    $ python3 fetch-company-info.py --tickers_filename "tickers.csv"

6. Company info is saved in json files in a "weekly" subfolder. Subsequent calls to fetch-company-info will skip companies that have already been fetched. (To re-fetch them delete the json file.)
7. Process the data from saved files.

    $ python3 process-company-info.py
