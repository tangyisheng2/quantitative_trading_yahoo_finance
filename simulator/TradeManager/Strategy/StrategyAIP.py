#  Copyright (c) 2023.
from simulator.TradeManager import TradeManager
from simulator.TradeManager.BaseStrategy import BaseStrategy, StrategyInterface
from simulator.Ticker.TickerFactory import TickerFactory
import datetime
import pandas


class StrategyAIP(BaseStrategy):
    tqqq_amount = 500
    hndl_amount = 500

    def __init__(self):
        super().__init__()

    def _get_first_monday_on_current_month(self, date: datetime.date) -> datetime.date:
        """
        This function returns the date of the first monday in current month
        :param date: date object for the month
        :return: date object for the first monday in current month
        """
        year = date.year
        month = date.month

        for day in range(1, 8):
            day_of_week = datetime.date(year, month, day).isoweekday()
            if day_of_week == 1:
                return datetime.date(year, month, day)

    def check(self, date: datetime.date = None, history_data: pandas.DataFrame = None) -> bool:
        first_monday = self._get_first_monday_on_current_month(date)
        return date.day == first_monday.day

    def execute(self, trade_manager: TradeManager, date: datetime.date = None) -> None:
        tqqq_ticker = TickerFactory.get_instance("TQQQ")
        hndl_ticker = TickerFactory.get_instance("HNDL")
        trade_manager.buy(tqqq_ticker, amount=self.tqqq_amount, on="Close", date=date)
        trade_manager.buy(hndl_ticker, amount=self.hndl_amount, on="Close", date=date)
