#  Copyright (c) 2023.
import datetime
import logging

import pandas as pd
from yfinance import Ticker

from simulator.Ticker.TickerInterface import TickerInterface

from typing import Optional


class BaseTicker(TickerInterface):
    ticker: Optional[Ticker] = None
    name: Optional[str] = None
    history: Optional[pd.DataFrame] = None
    holding: Optional[int] = None

    def __init__(self, ticker, name):
        # super().__init__(ticker, name)
        if not ticker or not name:
            raise AttributeError(f"Invalid attributes, got {ticker, name}")
        self._set_ticker(ticker)
        self._set_ticker_name(name)
        self.holding = 0

    def _set_ticker(self, ticker: Ticker) -> None:
        self.ticker = ticker

    def _set_ticker_name(self, name: str) -> None:
        self.name = name

    def get_history(self, period: str = "max") -> pd.DataFrame:
        ticker_history_df = self.ticker.history(period=period)
        # Get rid of the time and timezone from the ticker index
        ticker_history_df.index = ticker_history_df.index.date
        ticker_history_df.index.name = 'Date'

        self.history = ticker_history_df
        return self.history

    def get_data_on_date(self, date: datetime.date) -> pd.Series:
        if self.history is None:
            self.get_history()

        try:
            ans = self.history.loc[date]
        except KeyError:
            logging.warning("Can't fetch today's data before market close, fetch yesterdays data instead")
            ans = self.history.loc[date - datetime.timedelta(days=1)]

        return ans

    def buy(self, share: int, on: str) -> float:
        cur_date = datetime.date.today()

        data = self.get_data_on_date(date=cur_date)
        transaction_price = data.loc[on]

        if not transaction_price or transaction_price <= 0:
            raise ValueError(f"Invalid transaction price, got {transaction_price}, canceling transaction")
        self._increase_holding(share)
        return transaction_price * share

    def sell(self, share: int, on: str) -> float:
        if share > self.get_holding_shares():
            raise ValueError(
                f"Insufficient share in hold, you have {self.get_holding_shares()}, but trying to sell {share}, canceling transaction")

        cur_date = datetime.date.today()

        data = self.get_data_on_date(date=cur_date)
        transaction_price = data.loc[on]

        if not transaction_price or transaction_price <= 0:
            raise ValueError(f"Invalid transaction price, got {transaction_price}, canceling transaction")
        self._decrease_holding(share)
        return transaction_price * share

    def _increase_holding(self, share: int) -> bool:
        """
        This method increase the current holding.
        If the ticker object is not properly config, it throws a value error.
        :param share: The number of share to increase.
        :return: True is the operation is success.
        """
        if self.holding is None:
            raise ValueError(f"Invalid holding, the ticker is not properly config")
        self.holding += share
        return True

    def _decrease_holding(self, share: int) -> bool:
        """
        This method decrease the current holding.
        If the ticker object is not properly config, or the shares to decrease is more than the current holding,
        it throws a Value error
        :param share: The number of share to decrease.
        :return: True is the operation is success.
        """
        if self.holding is None:
            raise ValueError(f"Invalid holding, the ticker is not properly config")
        if share > self.get_holding_shares():
            raise ValueError(
                f"Insufficient share in hold, you have {self.get_holding_shares()}, but trying to sell {share}, canceling transaction")
        self.holding -= share
        return True

    def get_holding_shares(self) -> int:
        return self.holding

    def get_holding_values(self) -> float:
        close_price = self.get_data_on_date(datetime.date.today()).loc["Close"]
        return self.get_holding_shares() * close_price
