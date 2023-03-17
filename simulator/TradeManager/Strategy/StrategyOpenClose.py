#  Copyright (c) 2023.
from simulator.TradeManager import TradeManager
from simulator.TradeManager.BaseStrategy import BaseStrategy, StrategyInterface
from simulator.Ticker.TickerFactory import TickerFactory
from simulator.Wallet.BaseWallet import BaseWallet
import datetime
import pandas


class StrategyOpenClose(BaseStrategy):

    def __init__(self, wallet: BaseWallet = None):
        super().__init__(wallet=wallet)

    def _get_day_of_the_week(self, date: datetime.date) -> int:
        """
        This function returns the day of the week for $date
        :param date: query date
        :return: the day of the week
        """
        return date.isoweekday() == 1

    def check(self, date: datetime.date = None, history_data: pandas.DataFrame = None) -> bool:
        return self._get_day_of_the_week(date) == 1

    def execute(self, trade_manager: TradeManager, date: datetime.date = None) -> None:
        if self.wallet is None:
            self.logger.warning("Wallet is not set, can not run strategy")
            raise TypeError("Wallet is not set")
        try:
            tqqq_ticker = self.wallet.get_holding_ticker_by_name("TQQQ")
            tqqq_ticker_value = tqqq_ticker.get_holding_values(date=date)
            hndl_ticker = self.wallet.get_holding_ticker_by_name("HNDL")
            hndl_ticker_value = hndl_ticker.get_holding_values(date=date)
        except KeyError:
            return

        trade_manager.sell(tqqq_ticker, share=tqqq_ticker.get_holding_share_number(), on="Open", date=date)
        trade_manager.sell(hndl_ticker, share=hndl_ticker.get_holding_share_number(), on="Open", date=date)

        trade_manager.buy(tqqq_ticker, amount=tqqq_ticker_value, on="Close", date=date)
        trade_manager.buy(hndl_ticker, amount=hndl_ticker_value, on="Close", date=date)
