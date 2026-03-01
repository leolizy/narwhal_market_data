"""ICE (Intercontinental Exchange) adapter."""

from market_search.exchanges.base import ExchangeAdapter


class ICEAdapter(ExchangeAdapter):

    @property
    def exchange_name(self) -> str:
        return "Intercontinental Exchange (ICE)"

    @property
    def exchange_code(self) -> str:
        return "ICE"

    @property
    def clearing_house(self) -> str:
        return "ICE Clear Europe"

    def public_urls(self) -> dict:
        return {
            "product_list": "https://www.ice.com/products",
            "daily_price": "https://www.ice.com/marketdata/reports",
            "margin_rates": "https://www.ice.com/clear-europe/margin-rates",
            "exchange_fees": "https://www.ice.com/futures-europe/fees",
        }
