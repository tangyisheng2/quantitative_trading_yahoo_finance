#  Copyright (c) 2023.
import datetime

from common.Logger import Logger
from simulator.Ticker.BaseTicker import BaseTicker
from simulator.Wallet.WalletInterface import WalletInterface


class BaseWallet(WalletInterface):

    def __init__(self, initial_cash_value: float = 0):
        super().__init__()
        self._set_initial_cash(initial_cash_value)
        self.logger = Logger.get_logger(self.__class__.__name__)

    def _set_initial_cash(self, value: float) -> None:
        self.holding_cash = value

    def empty_cash(self) -> None:
        self.holding_cash = 0

    def get_cash_value(self) -> float:
        return self.holding_cash

    def get_total_asset_value(self, date: datetime.date = None) -> float:
        total_value = 0
        for name, ticker in self.holding_ticker.items():
            total_value += ticker.get_holding_values(date=date)
        total_value += self.holding_cash
        return total_value

    def add_cash_value(self, value: float) -> float:
        if value < 0:
            raise ValueError(f"Add cash value must be >= 0, got {value}")
        self.holding_cash += value
        return self.holding_cash

    def decrease_cash_value(self, value: float) -> float:
        if value < 0:
            raise ValueError(f"Decrease cash value must be >= 0, got {value}")

        if value > self.holding_cash:
            raise ValueError(f'Not enough money in the account, current balance: {self.holding_cash}')
        self.holding_cash -= value
        return self.holding_cash

    def update_ticker(self, ticker: BaseTicker) -> None:
        # Early return when the ticker to update is not in holding, and we are not holding any ticker
        if ticker.get_ticker_name() not in self.holding_ticker and ticker.get_holding_share_number() == 0:
            return
        if ticker.get_holding_share_number() == 0:
            del self.holding_ticker[ticker.get_ticker_name()]
        else:
            self.holding_ticker[ticker.get_ticker_name()] = ticker

    def get_holding_ticker_by_name(self, name: str) -> BaseTicker:
        """
        This method returns the ticker in the holding list.
        Ticker must be currently hold, or the method will raise a ValueError.
        :param name: Ticker name
        :return: ticker
        """
        return self.holding_ticker[name]

    def get_summary(self, date: datetime.date):
        return (
            f'Total: {self.get_total_asset_value(date)}, Cash: {self.get_cash_value()}, '
            f'Holding: {[{ticker.get_ticker_name(): {f"{ticker.get_holding_share_number()}, ${ticker.get_holding_values(date=date)}"}} for _, ticker in self.holding_ticker.items()]}')
