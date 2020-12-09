import datetime
import requests

# Holidays which the stock market is closed in 2021
holidays = ["2021-01-01",
            "2021-01-18",
            "2021-02-15",
            "2021-04-02",
            "2021-05-31",
            "2021-07-05",
            "2021-09-06",
            "2021-11-25",
            "2021-12-24"]


def grab_data(ticker: str) -> None:
    """
    Grab the minute-by-minute stock price for a given ticker symbol over the past 30 days
    :param ticker: The ticker of a stock to retrieve data from
    :return: None
    """

    file_object = open(ticker + "_1m.txt", 'w+')

    for days_prior in range(30):
        date = datetime.date.today() - datetime.timedelta(days_prior)
        if date.isoweekday() in range(1, 6) and date not in holidays:
            date = date.strftime("%Y%m%d")
            response = requests.get("https://sandbox.iexapis.com/stable/stock/" +
                                    ticker +
                                    "/chart/date/" +
                                    date +
                                    "?token=Tpk_8e791aca0b424ddfb17954a723f7c99a")
            data = response.json()
            for minute in data:
                file_object.write(str(minute["average"]) + "\n")
