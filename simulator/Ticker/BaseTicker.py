#  Copyright (c) 2023.
import datetime
import logging

import pandas as pd
from yfinance import Ticker

from common.Logger import Logger
from simulator.Ticker.TickerInterface import TickerInterface

from typing import Optional


class BaseTicker(TickerInterface):
    ticker: Optional[Ticker] = None
    name: Optional[str] = None
    history: Optional[pd.DataFrame] = None
    holding: Optional[int] = None

    def __init__(self, ticker: Ticker, name: str):
        super().__init__(ticker, name)
        if not ticker or not name:
            raise AttributeError(f"Invalid attributes, got {ticker, name}")
        self._set_ticker(ticker)
        self._set_ticker_name(name)
        self.holding = 0
        self.logger = Logger.get_logger(self.__class__.__name__)

    def _set_ticker(self, ticker: Ticker) -> None:
        self.ticker = ticker

    def _set_ticker_name(self, name: str) -> None:
        self.name = name

    def get_ticker_name(self) -> str:
        return self.name

    def get_history(self, period: str = "max") -> pd.DataFrame:
        ticker_history_df = self.ticker.history(period=period)
        # Get rid of the time and timezone from the ticker index
        ticker_history_df.index = ticker_history_df.index.date
        ticker_history_df.index.name = 'Date'

        self.history = ticker_history_df
        return self.history

    def get_data_on_date(self, date: datetime.date) -> pd.Series:
        # Always fetch the latest data to calculate the value
        self.get_history()

        try:
            ans = self.history.loc[date]
        except KeyError:
            ans = None

        return ans

    def buy(self, share: int, on: str, date: datetime.date = None) -> float:
        if not date:
            date = datetime.date.today()

        data = self.get_data_on_date(date=date)
        transaction_price = data.loc[on]

        if not transaction_price or transaction_price <= 0:
            raise ValueError(f"Invalid transaction price, got {transaction_price}, canceling transaction")
        self._increase_holding(share)
        return transaction_price * share

    def sell(self, share: int, on: str, date: datetime.date = None) -> float:
        if share > self.get_holding_share_number():
            raise ValueError(
                f"Insufficient share in hold, you have {self.get_holding_share_number()}, but trying to sell {share}, canceling transaction")

        if not date:
            date = datetime.date.today()

        data = self.get_data_on_date(date=date)
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
        if share > self.get_holding_share_number():
            raise ValueError(
                f"Insufficient share in hold, you have {self.get_holding_share_number()}, but trying to sell {share}, canceling transaction")
        self.holding -= share
        return True

    def get_holding_share_number(self) -> int:
        return self.holding

    def get_holding_values(self, date: datetime.date = None) -> float:
        if not date:
            date = datetime.date.today()
        try:
            close_price = self.get_data_on_date(date).loc["Close"]
            return self.get_holding_share_number() * float(close_price)
        except KeyError:
            logging.warning(f'Data not found at {date}')
        except AttributeError:
            return -1
