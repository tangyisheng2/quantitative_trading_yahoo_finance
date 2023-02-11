#  Copyright (c) 2023.
import datetime

import pandas

from simulator.TradeManager.TradeManager import TradeManager
from typing import Optional


class StrategyInterface:
    description: Optional[str] = None

    def __init__(self):
        pass

    def get_name(self):
        """
        This method returns the strategy name
        :return: the strategy name
        """
        raise NotImplementedError()

    def check(self, date: datetime.date = None, history_data: pandas.DataFrame = None) -> bool:
        """
        This method checks if the certain strategy is met.
        :param date: Date, for strategy based on the date
        :param history_data: History price data, for strategy based on the history data
        :return: Whether strategy is fulfilled
        """
        raise NotImplementedError()

    def execute(self, trade_manager: TradeManager) -> None:
        """
        This method executes the strategy.
        Put your strategy operation here.
        :param trade_manager: Trade Manager to handle the transaction
        :return:
        """
        raise NotImplementedError()
