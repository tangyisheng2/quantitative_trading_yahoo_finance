#  Copyright (c) 2023.
from simulator.TradeManager import TradeManager
from simulator.TradeManager.BaseStrategy import BaseStrategy, StrategyInterface
from simulator.Wallet.BaseWallet import BaseWallet
import datetime
import pandas


class StrategyRebalance(BaseStrategy):

    def __init__(self, wallet: BaseWallet = None):
        super().__init__(wallet=wallet)

    def _get_first_tuesday_on_current_month(self, date: datetime.date) -> datetime.date:
        """
        This function returns the date of the first tuesday in current month
        :param date: date object for the month
        :return: date object for the first tuesday in current month
        """
        year = date.year
        month = date.month

        for day in range(1, 8):
            day_of_week = datetime.date(year, month, day).isoweekday()
            if day_of_week == 2:
                return datetime.date(year, month, day)

    def check(self, date: datetime.date = None, history_data: pandas.DataFrame = None) -> bool:
        first_tuesday = self._get_first_tuesday_on_current_month(date)
        return date.month in [6, 12] and date.day == first_tuesday.day

    def execute(self, trade_manager: TradeManager, date: datetime.date = None) -> None:
        try:
            tqqq_ticker = self.wallet.get_holding_ticker_by_name("TQQQ")
            hndl_ticker = self.wallet.get_holding_ticker_by_name("HNDL")
        except KeyError:
            return

        diff = abs(tqqq_ticker.get_holding_values() - hndl_ticker.get_holding_values()) / 2

        self.logger.info(f"Diff: {diff}")

        if tqqq_ticker.get_holding_values() > hndl_ticker.get_holding_values():

            trade_manager.sell(tqqq_ticker, diff, on="Close", date=date)
            trade_manager.buy(hndl_ticker, diff, on="Close", date=date)
        else:
            trade_manager.buy(tqqq_ticker, diff, on="Close", date=date)
            trade_manager.sell(hndl_ticker, diff, on="Close", date=date)

        self.logger.info(f"Balanced: {tqqq_ticker.get_ticker_name()}-{tqqq_ticker.get_holding_values()},"
                         f"{hndl_ticker.get_ticker_name()}-{hndl_ticker.get_holding_values()}")
