#  Copyright (c) 2023.
import datetime

from simulator.Ticker.BaseTicker import BaseTicker as Ticker
from simulator.Wallet.BaseWallet import BaseWallet as Wallet
from simulator.TradeManager.TradeManagerInterface import TradeManagerInterface

from typing import Optional


class TradeManager(TradeManagerInterface):
    wallet: Optional[Wallet] = None

    def __init__(self):
        super().__init__()

    def set_wallet(self, wallet: Wallet):
        self.wallet = wallet

    def get_quote(self, ticker: Ticker, share: int = 0, on: str = "Close") -> float:
        price = ticker.get_data_on_date(datetime.date.today()).loc[on]
        quote = price * share
        return quote

    def buy(self, ticker: Ticker, share: int = 0, on: str = "Close") -> bool:
        transaction_total = self.get_quote(ticker, share, on)
        if self.wallet.get_cash_value() < transaction_total:
            raise ValueError(f"Insufficient fund, require {transaction_total}, but got {self.wallet.get_cash_value()}")
        actual_total = ticker.buy(share=share, on=on)
        assert transaction_total == actual_total
        self.wallet.decrease_cash_value(actual_total)
        self.wallet.update_ticker(ticker)
        return True

    def sell(self, ticker: Ticker, share: int = 0, on: str = "Close") -> bool:
        transaction_total = self.get_quote(ticker, share, on)
        if ticker.get_holding_share_number() < share:
            raise ValueError(
                f"Insufficient share holding, reuqire {share}, but currently have {ticker.get_holding_share_number()}")
        actual_total = ticker.sell(share=share, on=on)
        assert transaction_total == actual_total
        self.wallet.add_cash_value(actual_total)
        self.wallet.update_ticker(ticker)
        return True
