#  Copyright (c) 2023.

from simulator.TradeManager.BaseStrategy import BaseStrategy
from simulator.TradeManager.TradeManager import TradeManager
from simulator.Ticker.TickerFactory import TickerFactory
import datetime
import pandas


class StrategyAIPOn15thEveryMonth(BaseStrategy):
    def __init__(self):
        super().__init__()

    def check(self, date: datetime.date = None, history_data: pandas.DataFrame = None) -> bool:
        if date.isoweekday() in [6, 7]:
            next_monday_date = date
            while next_monday_date.isoweekday() > 1:
                next_monday_date += datetime.timedelta(days=1)
            return date.day == next_monday_date.day

        return date.day == 15

    def execute(self, trade_manager: TradeManager) -> None:
        tqqq_ticker = TickerFactory.get_instance("TQQQ")
        trade_manager.buy(ticker=tqqq_ticker, share=5, on="Close")
