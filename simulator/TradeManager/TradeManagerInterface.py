#  Copyright (c) 2023.
import datetime

from simulator.Ticker.BaseTicker import BaseTicker
from simulator.Wallet.BaseWallet import BaseWallet as Wallet


class TradeManagerInterface:
    def set_wallet(self, wallet: Wallet):
        """
        This method sets the wallet used in the operation (fund)
        :return:
        """
        raise NotImplementedError()

    def get_quote(self, ticker: BaseTicker, share: int = 0, on: str = "Close", date: datetime.date = None) -> float:
        """
        This method gets the quote for $share of $ticker
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param ticker: ticker
        :param share: number of the share
        :param date: The transaction date, if not specified, default to today
        :return: Quote for the transaction
        """
        raise NotImplementedError()

    def buy(self, ticker: BaseTicker, amount: float = 0, share: int = 0, on: str = "Close",
            date: datetime.date = None) -> bool:
        """
        This method buys $share of $ticker.
        It needs to verify if the ticker is valid, and if there is sufficient fund to complete the transaction
        :param ticker: ticker to buy
        :param amount: The amount of share to buy, use math.ceiling to determine how many shares to buy
        :param share: number of shares to buy (will be in higher priority compared to $amount)
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param date: The transaction date, if not specified, default to today
        :return: The transaction status, True -> success
        """
        raise NotImplementedError()

    def sell(self, ticker: BaseTicker, amount: float = 0, share: int = 0, on: str = "Close",
             date: datetime.date = None) -> bool:
        """
        This method sell $share of $ticker.
        It needs to verify if the ticker is valid, and if there is sufficient fund to complete the transaction
        :param ticker: ticker to buy
        :param amount: The amount of share to sell, use math.ceiling to determine how many shares to sell
        :param share: number of shares to buy (will be in higher priority compared to $amount)
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param date: The transaction date, if not specified, default to today
        :return: The transaction status, True -> success
        """
        raise NotImplementedError()
