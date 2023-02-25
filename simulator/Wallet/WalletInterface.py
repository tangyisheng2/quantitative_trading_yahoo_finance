#  Copyright (c) 2023.
import datetime
from typing import Dict
from simulator.Ticker.BaseTicker import BaseTicker


class WalletInterface:
    holding_ticker: Dict[str, BaseTicker] = {}
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

    def get_cash_value(self) -> float:
        """
        This method returns the cash value in the wallet
        :return: Cash value in the wallet
        """
        raise NotImplementedError()

    def get_total_asset_value(self, date: datetime.date = None) -> float:
        """
        This method calculates the total value of the assets in the account, including holding_ticker and the cash
        :param date: (Unittest) Calculate the holding assets based on the "Close" price of date,
                    if not specified, use today's price
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

    def update_ticker(self, ticker: BaseTicker) -> None:
        """
        This method updates the holding ticker property
        :param ticker: ticker to be updated
        :return: None
        """
        raise NotImplementedError()

    def get_holding_ticker_by_name(self, name: str) -> BaseTicker:
        """
        This method returns the ticker in the holding list.
        Ticker must be currently hold, or the method will raise a ValueError.
        :param name: Ticker name
        :return: ticker
        """
        raise NotImplementedError()
