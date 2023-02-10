#  Copyright (c) 2023.

import unittest

from simulator.Wallet.BaseWallet import BaseWallet


class BasicWaltletTest(unittest.TestCase):
    def test_create_wallet_should_success_with_initial_cash(self):
        initial_cash = 10000
        wallet = BaseWallet(initial_cash_value=initial_cash)
        self.assertTrue(type(wallet) == BaseWallet)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash)

    def test_create_wallet_should_success_without_initial_cash_and_have_0_cash(self):
        wallet = BaseWallet()
        self.assertTrue(type(wallet) == BaseWallet)
        self.assertEqual(wallet.get_total_asset_value(), 0)

    def test_empty_cash_should_work(self):
        initial_cash = 10000
        wallet = BaseWallet(initial_cash_value=initial_cash)
        self.assertTrue(type(wallet) == BaseWallet)
        self.assertEqual(wallet.get_total_asset_value(), initial_cash)
        wallet.empty_cash()
        self.assertEqual(wallet.get_total_asset_value(), 0)

    def test_get_total_asset_value_should_return_0(self):
        wallet = BaseWallet()
        self.assertTrue(type(wallet) == BaseWallet)
        self.assertEqual(wallet.get_total_asset_value(), 0)

    @unittest.skip("Reserve for future dev")
    def test_get_total_asset_value_should_return_correct_value(self):
        """
        1. Test when there is no cash and ticker
        2. Test when there is cash only
        3. Test when there are both cash and assets
        :return:
        """
        pass

    def test_should_add_value_to_the_wallet(self):
        wallet = BaseWallet()
        cash_value = 1000
        self.assertTrue(type(wallet) == BaseWallet)
        self.assertEqual(wallet.get_total_asset_value(), 0)
        wallet.add_cash_value(cash_value)
        self.assertEqual(wallet.get_total_asset_value(), cash_value)

    def test_should_decrease_value_to_the_wallet(self):
        wallet = BaseWallet()
        cash_value_increase = 1000
        cash_value_decrease = 500
        self.assertTrue(type(wallet) == BaseWallet)
        self.assertEqual(wallet.get_total_asset_value(), 0)
        wallet.add_cash_value(cash_value_increase)
        self.assertEqual(wallet.get_total_asset_value(), cash_value_increase)
        wallet.decrease_cash_value(cash_value_decrease)
        self.assertEqual(wallet.get_total_asset_value(), cash_value_increase - cash_value_decrease)

    def test_should_raise_error_when_decrease_more_than_the_balance(self):
        wallet = BaseWallet()
        cash_value_increase = 1000
        cash_value_decrease = 5000
        self.assertTrue(type(wallet) == BaseWallet)
        self.assertEqual(wallet.get_total_asset_value(), 0)
        wallet.add_cash_value(cash_value_increase)
        self.assertEqual(wallet.get_total_asset_value(), cash_value_increase)
        self.assertRaises(ValueError, lambda: wallet.decrease_cash_value(cash_value_decrease))
        self.assertEqual(wallet.get_total_asset_value(), cash_value_increase)


if __name__ == '__main__':
    unittest.main()
