#  Copyright (c) 2023.

from typing import Optional, List
from simulator.Ticker.BaseTicker import BaseTicker as Ticker


class WalletInterface:
    holding_ticker: List[Ticker] = []
    holding_cash = None

    def __init__(self):
        pass

    def _set_initial_cash(self, value: float) -> None:
        """
        This method sets the initial cash of the wallet
        :param value: Initial Cash amount
        :return: None
        """

        raise NotImplementedError()

    def empty_cash(self) -> None:
        """
        This method empty the cash wallet
        :return: None
        """
        raise NotImplementedError()

    def get_total_asset_value(self) -> float:
        """
        This method calculates the total value of the assets in the account, including holding_ticker and the cash
        :return: Total asset value
        """
        raise NotImplementedError()

    def add_cash_value(self, value: float) -> float:
        """
        This method adds increase the cash value by $value.
        It can use as a callback when selling a ticker.
        :param value: Value of cash to be added to the account
        :return: New account balance
        """
        raise NotImplementedError()

    def decrease_cash_value(self, value: float) -> float:
        """
        This method decrease the cash value by $value.
        It can use as a callback when buying a ticker.
        *It shou throws an ValueError when there is not enough cash in the account.*
        :param value: Value of cash to be decreased to the account.
        :return: New account balance
        """
        raise NotImplementedError()
