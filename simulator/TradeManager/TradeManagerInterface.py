#  Copyright (c) 2023.

from simulator.Ticker.BaseTicker import BaseTicker as Ticker
from simulator.Wallet.BaseWallet import BaseWallet as Wallet


class TradeManagerInterface:
    def set_wallet(self, wallet: Wallet):
        """
        This method sets the wallet used in the operation (fund)
        :return:
        """
        raise NotImplementedError()

    def get_quote(self, ticker: Ticker, share: int = 0, on: str = "Close") -> float:
        """
        This method gets the quote for $share of $ticker
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param ticker: ticker
        :param share: number of the share
        :return: Quote for the transaction
        """
        raise NotImplementedError()

    def buy(self, ticker: Ticker, share: int = 0, on: str = "Close") -> bool:
        """
        This method buys $share of $ticker.
        It needs to verify if the ticker is valid, and if there is sufficient fund to complete the transaction
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param ticker: ticker to buy
        :param share: number of shares to buy
        :return: The transaction status, True -> success
        """
        raise NotImplementedError()

    def sell(self, ticker: Ticker, share: int = 0, on: str = "Close") -> bool:
        """
        This method sell $share of $ticker.
        It needs to verify if the ticker is valid, and if there is sufficient fund to complete the transaction
        :param on: The price for this transaction, it can be ["Open", "Close", "High", "Low"]
        :param ticker: ticker to buy
        :param share: number of shares to buy
        :return: The transaction status, True -> success
        """
        raise NotImplementedError()
