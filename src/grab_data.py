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


def prepare_3_4_5_csv(ticker: str) -> None:
    """
    This function takes the minute by minute stock price of a ticker and pre-processes that data into a CSV format.
    The 3_4_5 format will take three consecutive stock prices, minute 1, 2 and 3 then determine if money would have
    been made if the stock corresponding to the ticker was bought on minute 4 and sold on minute 5.
    The CSV format is a follows:
    Minute 1 Price, Minute 2 Price, Minute 3 Price, Money Made (0 for no 1 for yes)
    :param ticker: A string representing the ticker of a stock
    :return: None
    """

    time2 = None
    time3 = None
    buy_price = None
    sell_price = None

    file_object = open(ticker + "3_4_5.txt", 'w+')

    counter = 0

    # read the corresponding file containing the minute by minute stock prices of a ticker
    with open(ticker + "_1m.txt") as file_in:
        for line in file_in:
            counter += 1
            time1 = time2
            time2 = time3
            time3 = buy_price
            buy_price = sell_price
            sell_price = line.strip()

            # Code needed for testing as test data contains None values
            if sell_price == "None":
                sell_price = "10"

            # Pre-processing begins after 5 points of data are loaded
            if not (counter > 4):
                continue

            if sell_price > buy_price:
                buy_sell = 1
            else:
                buy_sell = 0

            file_object.write(str(time1) + "," + str(time2) + "," + str(time3) + "," + str(buy_sell) + "\n")
    file_object.close()


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

    file_object.close()
