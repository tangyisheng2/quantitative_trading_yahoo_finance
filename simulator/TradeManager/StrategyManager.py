#  Copyright (c) 2023.
import datetime
from typing import List, Dict, Optional

import pandas

from common.Logger import Logger
from simulator.TradeManager.BaseStrategy import BaseStrategy as Strategy
from simulator.TradeManager.StrategyManagerInterface import StrategyManagerInterface
from simulator.TradeManager.TradeManager import TradeManager

from pandas.tseries.holiday import USFederalHolidayCalendar


class StrategyManager(StrategyManagerInterface):
    trade_manager: TradeManager

    def __init__(self, trade_manager: TradeManager):
        super().__init__()
        self.strategy_dict: Dict[str, Strategy] = {}
        self.trade_manager = trade_manager
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.holidays = USFederalHolidayCalendar().holidays().to_pydatetime()

    def add_strategy(self, strategy: Strategy) -> List[str]:
        strategy_name = strategy.get_name()
        self.strategy_dict[strategy_name] = strategy
        return list(self.strategy_dict.keys())

    def remove_strategy(self, strategy_name: str) -> List[str]:
        if strategy_name in self.strategy_dict:
            del self.strategy_dict[strategy_name]
        return list(self.strategy_dict.keys())

    def get_all_strategy(self) -> List[str]:
        return list(self.strategy_dict.keys())

    def check_and_run_strategy(self, date: datetime.date = None, history_data: pandas.DataFrame = None):
        if self._check_holiday(date):
            return

        for name, strategy in self.strategy_dict.items():
            if strategy.check(date=date, history_data=history_data):
                self.logger.info(f'Running strategy: {name}')
                strategy.execute(self.trade_manager, date=date)

    def _check_holiday(self, date: datetime.date):
        if datetime.datetime(date.year, date.month, date.day) in self.holidays:
            self.logger.warning(f'The day {date} is holiday, skipping.')
            return True
        return False
