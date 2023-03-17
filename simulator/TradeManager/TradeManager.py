#  Copyright (c) 2023.
import datetime
import logging
import math

import pandas as pd

from simulator.Ticker.BaseTicker import BaseTicker
from simulator.Wallet.BaseWallet import BaseWallet as Wallet
from simulator.TradeManager.TradeManagerInterface import TradeManagerInterface

from typing import Optional

from common.Logger import Logger

from pandas.tseries.holiday import USFederalHolidayCalendar


class TradeManager(TradeManagerInterface):
    wallet: Optional[Wallet] = None
    logger: logging.getLogger()

    def __init__(self):
        super().__init__()
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.holidays = USFederalHolidayCalendar().holidays().to_pydatetime()

    def set_wallet(self, wallet: Wallet):
        self.wallet = wallet

    def get_quote(self, ticker: BaseTicker, share: int = 0, on: str = "Close", date: datetime.date = None) -> Optional[
        float]:
        if not date:
            date = datetime.date.today()
        if self._check_holiday(date):
            return
        history = ticker.get_data_on_date(date)
        if history is not None:
            price = ticker.get_data_on_date(date).loc[on]
            quote = price * share
            return quote
        return None

    def _check_holiday(self, date: datetime.date):
        if date.isoweekday() in {6, 7} or datetime.datetime(date.year, date.month, date.day) in self.holidays:
            return True
        return False

    def buy(self, ticker: BaseTicker, amount: float = 0, share: int = 0, on: str = "Close",
            date: datetime.date = None) -> bool:

        if not date:
            date = datetime.date.today()

        if self._check_holiday(date):
            return False

        price_per_share = self.get_quote(ticker, 1, on, date=date)

        if not price_per_share:  # If there is no valid price, do not make the transaction
            return False

        if amount > 0 and not share:
            share = math.floor(amount / price_per_share)

        transaction_total = self.get_quote(ticker, share, on, date=date)
        if self.wallet.get_cash_value() < transaction_total:
            raise ValueError(f"Insufficient fund, require {transaction_total}, but got {self.wallet.get_cash_value()}")
        actual_total = ticker.buy(share=share, on=on, date=date)
        assert abs(transaction_total - actual_total) < 0.01  # Omit the very slight price diff
        self.wallet.decrease_cash_value(actual_total)
        self.wallet.update_ticker(ticker)
        self.logger.info(
            f'{date}: Bought {ticker.get_ticker_name()} * {share}shares @ {price_per_share} (on {on}), total: {price_per_share * share}')
        return True

    def sell(self, ticker: BaseTicker, amount: float = 0, share: int = 0, on: str = "Close",
             date: datetime.date = None) -> bool:

        if not date:
            date = datetime.date.today()

        if self._check_holiday(date):
            return False

        price_per_share = self.get_quote(ticker, 1, on, date=date)

        if not price_per_share:  # If there is no valid price, do not make the transaction
            return False

        if amount > 0 and not share:
            share = math.floor(amount / price_per_share)

        transaction_total = self.get_quote(ticker, share, on, date=date)
        if ticker.get_holding_share_number() < share:
            raise ValueError(
                f"Insufficient share holding, reuqire {share}, but currently have {ticker.get_holding_share_number()}")
        actual_total = ticker.sell(share=share, on=on, date=date)
        assert abs(transaction_total - actual_total) < 0.01  # Omit the very slight price diff
        self.wallet.add_cash_value(actual_total)
        self.wallet.update_ticker(ticker)
        self.logger.info(
            f'{date}: Sold {ticker.get_ticker_name()} * {share}shares @ {price_per_share} (on {on}), total: {price_per_share * share}')
        return True
