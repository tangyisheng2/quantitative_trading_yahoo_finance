#  Copyright (c) 2023.
import datetime

import pandas

from simulator.TradeManager.StrategyInterface import StrategyInterface
from simulator.TradeManager.TradeManager import TradeManager


class BaseStrategy(StrategyInterface):

    def __init__(self, description: str = None):
        """
        Sets some description of the BaseStrategy
        :param description:
        """
        super().__init__()
        self.description = description
        self.name = self.__class__.__name__

    def get_name(self):
        return self.name

    def check(self, date: datetime.date = None, history_data: pandas.DataFrame = None) -> bool:
        pass

    def execute(self, trade_manager: TradeManager) -> None:
        pass
