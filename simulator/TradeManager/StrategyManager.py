#  Copyright (c) 2023.
import datetime
from typing import List, Dict, Optional

import pandas

from simulator.TradeManager.BaseStrategy import BaseStrategy as Strategy
from simulator.TradeManager.StrategyManagerInterface import StrategyManagerInterface
from simulator.TradeManager.TradeManager import TradeManager


class StrategyManager(StrategyManagerInterface):
    trade_manager: TradeManager

    def __init__(self, trade_manager: TradeManager):
        super().__init__()
        self.strategy_dict: Dict[str, Strategy] = {}
        self.trade_manager = trade_manager

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
        for name, strategy in self.strategy_dict.items():
            if strategy.check(date=date, history_data=history_data):
                strategy.execute(self.trade_manager)
