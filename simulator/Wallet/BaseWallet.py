#  Copyright (c) 2023.

from simulator.Wallet.WalletInterface import WalletInterface


class BaseWallet(WalletInterface):
    def __init__(self, initial_cash_value: float = 0):
        super().__init__()
        self._set_initial_cash(initial_cash_value)

    def _set_initial_cash(self, value: float) -> None:
        self.holding_cash = value

    def empty_cash(self) -> None:
        self.holding_cash = 0

    def get_total_asset_value(self) -> float:
        total_value = 0
        for ticker in self.holding_ticker:
            total_value += ticker.get_holding_values()
        total_value += self.holding_cash
        return total_value

    def add_cash_value(self, value: float) -> float:
        if value < 0:
            raise ValueError(f"Add cash value must be >= 0, got {value}")
        self.holding_cash += value
        return self.holding_cash

    def decrease_cash_value(self, value: float) -> float:
        if value < 0:
            raise ValueError(f"Decrease cash value must be >= 0, got {value}")

        if value > self.holding_cash:
            raise ValueError(f'Not enough money in the account, current balance: {self.holding_cash}')
        self.holding_cash -= value
        return self.holding_cash
