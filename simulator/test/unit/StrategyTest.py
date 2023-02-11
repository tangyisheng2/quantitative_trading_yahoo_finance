#  Copyright (c) 2023.
#  Copyright (c) 2023.
import datetime
import unittest


class StrategyTest(unittest.TestCase):
    def test_StrategyAIPOn15thEveryMonth_should_meet_on_15th_every_month(self):
        from simulator.TradeManager.Strategy.StrategyAIPOn15thEveryMonth import StrategyAIPOn15thEveryMonth
        strategy = StrategyAIPOn15thEveryMonth()
        self.assertTrue(strategy.check(datetime.datetime.strptime("2023-01-15", "%Y-%m-%d")))
        self.assertFalse(strategy.check(datetime.datetime.strptime("2023-01-16", "%Y-%m-%d")))

    def test_StrategyAIPOn15thEveryMonth_should_execute_on_15th_every_month(self):
        from simulator.TradeManager.Strategy.StrategyAIPOn15thEveryMonth import StrategyAIPOn15thEveryMonth
        from simulator.TradeManager.TradeManager import TradeManager
        from simulator.Wallet.BaseWallet import BaseWallet
        # Config
        wallet_init_cash = 10000
        date = datetime.datetime.strptime("2023-01-15", "%Y-%m-%d")
        # End Config
        wallet = BaseWallet(wallet_init_cash)
        trade_manager = TradeManager()
        trade_manager.set_wallet(wallet)
        strategy = StrategyAIPOn15thEveryMonth()
        self.assertTrue(strategy.check(date))
        if strategy.check(date):
            strategy.execute(trade_manager=trade_manager)
        self.assertEqual(wallet.get_total_asset_value(), wallet_init_cash)
        self.assertEqual(wallet.holding_ticker["TQQQ"].get_holding_share_number(), 5)




if __name__ == '__main__':
    unittest.main()
