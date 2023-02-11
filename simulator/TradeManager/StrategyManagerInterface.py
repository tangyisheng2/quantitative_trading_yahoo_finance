#  Copyright (c) 2023.
import datetime

import pandas

from simulator.TradeManager.BaseStrategy import BaseStrategy as Strategy

from typing import List


class StrategyManagerInterface:
    def __init__(self):
        pass

    def add_strategy(self, strategy: Strategy) -> List[str]:
        """
        This method adds a certain strategy to collection
        :param strategy: Strategy to be added
        :return: New strategy list
        """
        raise NotImplementedError()

    def remove_strategy(self, strategy_name: str) -> List[str]:
        """
        This method removes a certain strategy to collection
        :param strategy_name: Strategy name to be removed
        :return: New strategy list
        """
        raise NotImplementedError()

    def get_all_strategy(self) -> List[str]:
        """
        This method returns a list of all added strategy name
        :return: a list of all added strategy name
        """
        raise NotImplementedError()

    def check_and_run_strategy(self, date: datetime.date = None, history_data: pandas.DataFrame = None):
        """
        This method checks all added strategy and run the strategy when criteria is met.
        :return:
        """
        raise NotImplementedError()
