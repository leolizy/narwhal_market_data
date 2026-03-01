"""London Metal Exchange (LME) adapter."""

from market_search.exchanges.base import ExchangeAdapter


class LMEAdapter(ExchangeAdapter):

    @property
    def exchange_name(self) -> str:
        return "London Metal Exchange (LME)"

    @property
    def exchange_code(self) -> str:
        return "LME"

    @property
    def clearing_house(self) -> str:
        return "LME Clear"

    def public_urls(self) -> dict:
        return {
            "product_list": "https://www.lme.com/en/metals",
            "daily_price": "https://www.lme.com/en/market-data/reports-and-data",
            "margin_rates": "https://www.lme.com/en/clearing/margin",
            "exchange_fees": "https://www.lme.com/en/about/fees",
        }
