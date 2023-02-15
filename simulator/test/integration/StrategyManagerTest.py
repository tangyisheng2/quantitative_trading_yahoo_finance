#  Copyright (c) 2023.
import logging
import unittest
from common.Logger import Logger


class StrategyManagerTest(unittest.TestCase):

    @unittest.skip("Skip because strategy is not enabled")
    def test_add_StrategyAIPOn15thEveryMonth_should_work(self):
        import datetime

        from simulator.TradeManager.TradeManager import TradeManager
        from simulator.TradeManager.StrategyManager import StrategyManager
        from simulator.Wallet.BaseWallet import BaseWallet

        from simulator.TradeManager.Strategy.StrategyAIPOn15thEveryMonth import StrategyAIPOn15thEveryMonth
        # Config
        wallet_init_cash = 10000
        date = datetime.datetime.strptime("2023-01-17", "%Y-%m-%d").date()
        # End Config
        # Set up env
        wallet = BaseWallet(initial_cash_value=wallet_init_cash)
        trade_manager = TradeManager()
        trade_manager.set_wallet(wallet)
        strategy_manager = StrategyManager(trade_manager)
        logger = Logger().get_logger()
        # Add strategy
        strategy = StrategyAIPOn15thEveryMonth()
        strategy_manager.add_strategy(strategy)
        self.assertEqual(strategy_manager.get_all_strategy(), [strategy.get_name()])

        # Test strategy
        self.assertTrue(strategy.check(date))
        strategy.execute(trade_manager=trade_manager)
        self.assertEqual(wallet.get_total_asset_value(date=date), wallet_init_cash)
        self.assertEqual(wallet.holding_ticker["TQQQ"].get_holding_share_number(), 5)

    def test_StrategyAIP_should_work(self):
        import datetime

        from simulator.TradeManager.TradeManager import TradeManager
        from simulator.TradeManager.StrategyManager import StrategyManager
        from simulator.Wallet.BaseWallet import BaseWallet

        from simulator.TradeManager.Strategy.StrategyAIP import StrategyAIP
        # Config
        wallet_init_cash = 10000
        date_should_run = datetime.datetime.strptime("2023-02-06", "%Y-%m-%d").date()
        date_should_not_run = datetime.datetime.strptime("2023-02-13", "%Y-%m-%d").date()
        # End Config
        # Set up env
        wallet = BaseWallet(initial_cash_value=wallet_init_cash)
        trade_manager = TradeManager()
        trade_manager.set_wallet(wallet)
        strategy_manager = StrategyManager(trade_manager)

        # Add strategy
        strategy = StrategyAIP()
        strategy_manager.add_strategy(strategy)
        self.assertEqual(strategy_manager.get_all_strategy(), [strategy.get_name()])

        # Test strategy
        self.assertTrue(strategy.check(date_should_run))
        self.assertFalse(strategy.check(date_should_not_run))
        strategy.execute(trade_manager=trade_manager, date=date_should_run)
        self.assertEqual(wallet.get_total_asset_value(date=date_should_run), wallet_init_cash)

        tqqq_should_buy_shares = strategy.tqqq_amount // \
                                 trade_manager.wallet.holding_ticker['TQQQ'].history.loc[date_should_run].loc[
                                     "Close"]
        hndl_should_buy_shares = strategy.hndl_amount // \
                                 trade_manager.wallet.holding_ticker['HNDL'].history.loc[date_should_run].loc[
                                     "Close"]

        self.assertEqual(wallet.holding_ticker["TQQQ"].get_holding_share_number(), tqqq_should_buy_shares)
        self.assertEqual(wallet.holding_ticker["HNDL"].get_holding_share_number(), hndl_should_buy_shares)


if __name__ == '__main__':
    unittest.main()
