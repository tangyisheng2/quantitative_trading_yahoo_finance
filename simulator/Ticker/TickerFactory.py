#  Copyright (c) 2023.

from common import Singleton
from simulator.Ticker.BaseTicker import BaseTicker
import yfinance as yf


class TickerFactory(Singleton):

    @staticmethod
    def get_instance(ticker_name: str) -> BaseTicker:
        yfinance_ticker = yf.Ticker(ticker_name)
        ticker = BaseTicker(ticker=yfinance_ticker, name=ticker_name)
        return ticker

