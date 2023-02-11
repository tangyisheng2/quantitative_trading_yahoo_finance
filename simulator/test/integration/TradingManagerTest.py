#  Copyright (c) 2023.
import math
import unittest
from yfinance import Ticker
from simulator.Wallet.BaseWallet import BaseWallet as Wallet
from simulator.TradeManager.TradeManager import TradeManager
from simulator.Ticker.TickerFactory import TickerFactory


class TradingManagerTest(unittest.TestCase):
    def test_get_quote_should_success(self):
        # CONFIG
        initial_cash_value = 10000
        transaction_shares = 5
        transaction_on = "Close"
        # END-CONFIG
        # GET QUOTE
        ticker = Ticker("TQQQ")
        price = ticker.history(period='1d').iloc[0].loc[transaction_on]
        reference_quote = price * transaction_shares
        # END GET QUOTE
        # SET UP TRADE MANAGER
        trade_mgr = TradeManager()
        wallet = Wallet(initial_cash_value=initial_cash_value)
        trade_mgr.set_wallet(wallet)
        # END SET UP TRADE MANAGER
        actual_quote = trade_mgr.get_quote(ticker=TickerFactory.get_instance("TQQQ"), share=transaction_shares,
                                           on=transaction_on)
        self.assertEqual(reference_quote, actual_quote)

    def test_buy_stock_should_success(self):
        # CONFIG
        initial_cash_value = 10000
        transaction_shares = 5
        transaction_on = "Close"
        # END-CONFIG
        # SET UP TRADE MANAGER
        trade_mgr = TradeManager()
        wallet = Wallet(initial_cash_value=initial_cash_value)
        trade_mgr.set_wallet(wallet)
        base_ticker = TickerFactory.get_instance("TQQQ")
        # END SET UP TRADE MANAGER
        # GET QUOTE
        quote = trade_mgr.get_quote(base_ticker, transaction_shares, transaction_on)
        # END GET QUOTE

        status = trade_mgr.buy(ticker=base_ticker, share=transaction_shares, on=transaction_on)
        self.assertTrue(status)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - quote)

    def test_buy_stock_without_fund_should_failed(self):
        # CONFIG
        initial_cash_value = 0
        transaction_shares = 5
        transaction_on = "Close"
        # END-CONFIG
        # SET UP TRADE MANAGER
        trade_mgr = TradeManager()
        wallet = Wallet(initial_cash_value=initial_cash_value)
        trade_mgr.set_wallet(wallet)
        base_ticker = TickerFactory.get_instance("TQQQ")
        # END SET UP TRADE MANAGER
        # GET QUOTE
        quote = trade_mgr.get_quote(base_ticker, transaction_shares, transaction_on)
        # END GET QUOTE

        self.assertRaises(ValueError,
                          lambda: trade_mgr.buy(ticker=base_ticker, share=transaction_shares, on=transaction_on))

    def test_sell_stock_should_success(self):
        # CONFIG
        initial_cash_value = 10000
        buy_shares = 5
        buy_on = "Close"
        sell_shares = 3
        sell_on = "Close"
        # END-CONFIG
        # SET UP TRADE MANAGER
        trade_mgr = TradeManager()
        wallet = Wallet(initial_cash_value=initial_cash_value)
        trade_mgr.set_wallet(wallet)
        base_ticker = TickerFactory.get_instance("TQQQ")
        # END SET UP TRADE MANAGER
        # GET QUOTE
        buy_quote = trade_mgr.get_quote(base_ticker, buy_shares, buy_on)
        sell_quote = trade_mgr.get_quote(base_ticker, sell_shares, sell_on)
        # END GET QUOTE
        # BUY TICKER
        status = trade_mgr.buy(ticker=base_ticker, share=buy_shares, on=buy_on)
        self.assertTrue(status)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - buy_quote)
        # END BUY TICKER
        # SELL TICKER
        status = trade_mgr.sell(ticker=base_ticker, share=sell_shares, on=sell_on)
        self.assertTrue(status)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(base_ticker.get_holding_share_number(), buy_shares - sell_shares)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - buy_quote + sell_quote)
        # END SELL TICKER

    def test_overselling_stock_should_failed(self):
        # CONFIG
        initial_cash_value = 10000
        buy_shares = 5
        buy_on = "Close"
        sell_shares = 10
        sell_on = "Close"
        # END-CONFIG
        # SET UP TRADE MANAGER
        trade_mgr = TradeManager()
        wallet = Wallet(initial_cash_value=initial_cash_value)
        trade_mgr.set_wallet(wallet)
        base_ticker = TickerFactory.get_instance("TQQQ")
        # END SET UP TRADE MANAGER
        # GET QUOTE
        buy_quote = trade_mgr.get_quote(base_ticker, buy_shares, buy_on)
        sell_quote = trade_mgr.get_quote(base_ticker, sell_shares, sell_on)
        # END GET QUOTE
        # BUY TICKER
        status = trade_mgr.buy(ticker=base_ticker, share=buy_shares, on=buy_on)
        self.assertTrue(status)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - buy_quote)
        # END BUY TICKER
        # SELL TICKER
        self.assertRaises(ValueError, lambda: trade_mgr.sell(ticker=base_ticker, share=sell_shares, on=sell_on))
        # END SELL TICKER
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - buy_quote)

    def test_buying_stock_by_amount_should_success(self):
        # CONFIG
        initial_cash_value = 10000
        transaction_amount = 500
        transaction_on = "Close"
        # END-CONFIG
        # SET UP TRADE MANAGER
        trade_mgr = TradeManager()
        wallet = Wallet(initial_cash_value=initial_cash_value)
        trade_mgr.set_wallet(wallet)
        base_ticker = TickerFactory.get_instance("TQQQ")
        # END SET UP TRADE MANAGER
        # GET QUOTE
        quote = trade_mgr.get_quote(base_ticker, 1, transaction_on)
        # END GET QUOTE
        reference_share_number = math.ceil(transaction_amount / quote)
        status = trade_mgr.buy(ticker=base_ticker, amount=transaction_amount, on=transaction_on)
        self.assertTrue(status)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - quote * reference_share_number)

    def test_sell_stock_by_amount_should_success(self):
        # CONFIG
        initial_cash_value = 10000
        buy_shares = 100
        buy_on = "Close"
        sell_amount = 100
        sell_on = "Close"
        # END-CONFIG
        # SET UP TRADE MANAGER
        trade_mgr = TradeManager()
        wallet = Wallet(initial_cash_value=initial_cash_value)
        trade_mgr.set_wallet(wallet)
        base_ticker = TickerFactory.get_instance("TQQQ")
        # END SET UP TRADE MANAGER
        # GET QUOTE
        buy_quote = trade_mgr.get_quote(base_ticker, buy_shares, buy_on)
        selling_price_per_share = trade_mgr.get_quote(base_ticker, 1, sell_on)
        sell_share = math.ceil(sell_amount / selling_price_per_share)
        # END GET QUOTE
        # BUY TICKER
        status = trade_mgr.buy(ticker=base_ticker, share=buy_shares, on=buy_on)
        self.assertTrue(status)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - buy_quote)
        # END BUY TICKER
        # SELL TICKER
        status = trade_mgr.sell(ticker=base_ticker, amount=sell_amount, on=sell_on)
        self.assertTrue(status)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash_value)
        self.assertEqual(base_ticker.get_holding_share_number(), buy_shares - sell_share)
        self.assertEqual(wallet.get_cash_value(), initial_cash_value - buy_quote + sell_share * selling_price_per_share)


if __name__ == '__main__':
    unittest.main()
