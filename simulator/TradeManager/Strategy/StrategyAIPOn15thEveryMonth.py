#  Copyright (c) 2023.

from simulator.TradeManager.BaseStrategy import BaseStrategy
from simulator.TradeManager.TradeManager import TradeManager
from simulator.Ticker.TickerFactory import TickerFactory
import datetime
import pandas


class StrategyAIPOn15thEveryMonth(BaseStrategy):
    def check(self, date: datetime.date = None, history_data: pandas.DataFrame = None) -> bool:
        return date.day == 15

    def execute(self, trade_manager: TradeManager) -> None:
        tqqq_ticker = TickerFactory.get_instance("TQQQ")
        trade_manager.buy(ticker=tqqq_ticker, share=5, on="Close")
