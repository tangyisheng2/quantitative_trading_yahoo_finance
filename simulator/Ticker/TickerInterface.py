#  Copyright (c) 2023.
import datetime

import pandas as pd

from yfinance import Ticker


class TickerInterface:
    def __init__(self, ticker: Ticker, name: str):
        """
        This constructor sets the ticker object and its name
        """
        pass

    def _set_ticker(self, ticker: Ticker) -> None:
        """
        This method injects the ticker object to the class.
        :param ticker: ticker object
        """
        raise NotImplementedError()

    def _set_ticker_name(self, name: str) -> None:
        """
        This method sets the name of the ticker
        :param name:
        :return:
        """
        raise NotImplementedError()

    def get_ticker_name(self) -> str:
        """
        This method returns the ticker-name
        :return: The name of the ticker
        """
        raise NotImplementedError()

    def get_history(self, period: str = "max") -> pd.DataFrame:
        """
        This method get the history in period.
        Data including Open, High, Low, Close, Volume, Dividends, Stock Splits, Capital gains
        :param period: period of the history, default is max.
        :return: Data including Open, High, Low, Close, Volume, Dividends, Stock Splits, Capital gains
        """

        raise NotImplementedError()

    def get_data_on_date(self, date: datetime.date) -> pd.Series:
        """
        This method get the data on a certain date.
        :param date: Date
        :return:
        """
        raise NotImplementedError()

    def buy(self, share: int, on: str, date: datetime.date = None) -> float:
        """
        This method buys the ticker and returns the cost.
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param share: the number of share to buy
        :param date: The transaction date, if not specified, default to today
        :return: cost of the transaction
        """
        raise NotImplementedError()

    def sell(self, share: int, on: str, date: datetime.date = None) -> float:
        """
        This method sells the ticker and returns the cost
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param share:
        :param date: The transaction date, if not specified, default to today
        :return:
        """
        raise NotImplementedError()

    def get_holding_share_number(self) -> int:
        """
        This method gets the holding shares for the current ticker.
        :return: The number of current holding shares
        """
        raise NotImplementedError()

    def get_holding_values(self, date: datetime.date = None) -> float:
        """
        This method gets the value of the total holding shares.
        :param date: (Unittest) Calculate the holding assets based on the "Close" price of date,
                    if not specified, use today's price
        :return: The total value of the holding
        """
        raise NotImplementedError()
