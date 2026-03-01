"""Eurex adapter."""

from market_search.exchanges.base import ExchangeAdapter


class EurexAdapter(ExchangeAdapter):

    @property
    def exchange_name(self) -> str:
        return "Eurex"

    @property
    def exchange_code(self) -> str:
        return "EUREX"

    @property
    def clearing_house(self) -> str:
        return "Eurex Clearing"

    def public_urls(self) -> dict:
        return {
            "product_list": "https://www.eurex.com/ex-en/markets",
            "daily_price": "https://www.eurex.com/ex-en/data/statistics/market-statistics-online",
            "margin_rates": "https://www.eurex.com/ex-en/clearing/risk-management",
            "exchange_fees": "https://www.eurex.com/ex-en/rules-regs/eurex-exchange-fees",
        }
