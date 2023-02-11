#  Copyright (c) 2023.
import datetime
import unittest


class TickerTest(unittest.TestCase):
    def test_one_plus_one_should_equal_two(self):
        self.assertEqual(1 + 1, 2)

    def test_history_index_only_contains_date(self):
        from simulator.Ticker.TickerFactory import TickerFactory
        factory_tqqq_history = TickerFactory.get_instance("TQQQ").get_history()
        self.assertEqual(factory_tqqq_history.index.dtype, datetime.date)

    def test_ticker_factory_should_return_TQQQ_ticker(self):
        import yfinance as yf
        from simulator.Ticker.TickerFactory import TickerFactory
        import numpy as np
        # Create reference
        ticker = yf.Ticker("TQQQ")
        ticker = ticker.history(period='max')
        # Keep the date only in the index
        ticker.index = ticker.index.date
        ticker.index.name = 'Date'

        factory_ticker_history_df = TickerFactory.get_instance("TQQQ").get_history()

        # Create the object
        self.assertTrue(np.isclose(ticker.iloc[0], factory_ticker_history_df.iloc[0]).all())

    def test_ticker_factory_should_return_HNDL_ticker(self):
        import yfinance as yf
        from simulator.Ticker.TickerFactory import TickerFactory
        import numpy as np
        # Create reference
        ticker = yf.Ticker("HNDL")
        ticker_df = ticker.history(period='max')
        # Keep the date only in the index
        ticker_df.index = ticker_df.index.date
        ticker_df.index.name = 'Date'

        factory_ticker_history_df = TickerFactory.get_instance("HNDL").get_history()

        # Create the object
        self.assertTrue(np.isclose(ticker_df.iloc[0], factory_ticker_history_df.iloc[0]).all())

    def test_increase_holding_should_success(self):
        from simulator.Ticker.TickerFactory import TickerFactory
        # Config
        share = 30
        price_on = "Open"
        # Config END
        ticker = TickerFactory.get_instance("TQQQ")
        price_data = ticker.get_data_on_date(datetime.date.today())
        price = price_data.loc[price_on]
        self.assertEqual(ticker.get_holding_share_number(), 0)
        # Test the increase function
        cost = ticker.buy(share=share, on=price_on)
        self.assertEqual(cost, share * price)
        self.assertEqual(ticker.get_holding_share_number(), share)

    def test_decrease_less_holding_than_current_should_success(self):
        from simulator.Ticker.TickerFactory import TickerFactory
        # BUY Config
        buy_share = 30
        buy_price_on = "Open"
        # BUY Config END
        # SELL Config
        sell_share = 25
        sell_price_on = "Close"
        # SELL Config END
        ticker = TickerFactory.get_instance("TQQQ")
        price_data = ticker.get_data_on_date(datetime.date.today())
        buy_price = price_data.loc[buy_price_on]
        self.assertEqual(ticker.get_holding_share_number(), 0)
        # Test the increase function
        cost = ticker.buy(share=buy_share, on=buy_price_on)
        self.assertEqual(cost, buy_share * buy_price)
        self.assertEqual(ticker.get_holding_share_number(), buy_share)
        # Test the decrease function
        sell_price = price_data.loc[sell_price_on]
        self.assertEqual(ticker.get_holding_share_number(), buy_share)
        earn = ticker.sell(share=sell_share, on=sell_price_on)
        self.assertEqual(earn, sell_share * sell_price)
        self.assertEqual(ticker.get_holding_share_number(), buy_share - sell_share)

    def test_decrease_more_holding_than_current_should_failed(self):
        from simulator.Ticker.TickerFactory import TickerFactory
        # BUY Config
        buy_share = 30
        buy_price_on = "Open"
        # BUY Config END
        # SELL Config
        sell_share = 40
        sell_price_on = "Close"
        # SELL Config END
        ticker = TickerFactory.get_instance("TQQQ")
        price_data = ticker.get_data_on_date(datetime.date.today())
        buy_price = price_data.loc[buy_price_on]
        self.assertEqual(ticker.get_holding_share_number(), 0)
        # Test the increase function
        cost = ticker.buy(share=buy_share, on=buy_price_on)
        self.assertEqual(cost, buy_share * buy_price)
        self.assertEqual(ticker.get_holding_share_number(), buy_share)
        # Test the decrease function
        self.assertEqual(ticker.get_holding_share_number(), buy_share)
        self.assertRaises(ValueError, lambda: ticker.sell(sell_share, sell_price_on))

    def test_get_today_data_before_close_should_not_have_error(self):
        from simulator.Ticker.TickerFactory import TickerFactory
        import datetime
        ticker = TickerFactory.get_instance("TQQQ")
        ticker.get_data_on_date(datetime.date.today())
        # Succeed when no error raises

    def test_ticker_value_calculation_overtime_should_success(self):
        import datetime
        from simulator.Ticker.BaseTicker import BaseTicker
        import pandas as pd
        # Set current date
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)

        # Construct Mock Ticker class
        class Ticker:
            def __init__(self):
                self._history = None

            def history(self, period):
                return self._history

            def test_set_history(self, data: pd.DataFrame):
                self._history = data

        ticker = Ticker()
        base_ticker = BaseTicker(ticker=ticker, name="test")
        base_ticker.holding = 1

        ticker.test_set_history(pd.DataFrame(data=[[0, 0, 0, 10, 0, 0, 0, 0]
                                                   ],
                                             index=[yesterday],
                                             columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends',
                                                      'Stock Splits',
                                                      'Capital Gains']))

        self.assertEqual(base_ticker.get_holding_values(), 10)

        ticker.test_set_history(pd.DataFrame(data=[[0, 0, 0, 10, 0, 0, 0, 0],
                                                   [0, 0, 0, 20, 0, 0, 0, 0]],
                                             index=[yesterday, today],
                                             columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends',
                                                      'Stock Splits',
                                                      'Capital Gains']))

        self.assertEqual(base_ticker.get_holding_values(), 20)


if __name__ == '__main__':
    unittest.main()
