#  Copyright (c) 2023.

import unittest


class StrategyManagerTest(unittest.TestCase):
    def test_add_StrategyAIPOn15thEveryMonth_should_work(self):
        import datetime

        from simulator.TradeManager.TradeManager import TradeManager
        from simulator.TradeManager.StrategyManager import StrategyManager
        from simulator.Wallet.BaseWallet import BaseWallet

        from simulator.TradeManager.Strategy.StrategyAIPOn15thEveryMonth import StrategyAIPOn15thEveryMonth
        # Config
        wallet_init_cash = 10000
        date = datetime.datetime.strptime("2023-01-15", "%Y-%m-%d")
        # End Config
        # Set up env
        wallet = BaseWallet(initial_cash_value=wallet_init_cash)
        trade_manager = TradeManager()
        trade_manager.set_wallet(wallet)
        strategy_manager = StrategyManager(trade_manager)
        # Add strategy
        strategy = StrategyAIPOn15thEveryMonth()
        strategy_manager.add_strategy(strategy)
        self.assertEqual(strategy_manager.get_all_strategy(), [strategy.get_name()])
        # Test strategy
        self.assertTrue(strategy.check(date))
        if strategy_manager.check_and_run_strategy(date):
            strategy.execute(trade_manager=trade_manager)
        self.assertEqual(wallet.get_total_asset_value(), wallet_init_cash)
        self.assertEqual(wallet.holding_ticker["TQQQ"].get_holding_share_number(), 5)


if __name__ == '__main__':
    unittest.main()
