"""Australian Securities Exchange (ASX) adapter."""

from market_search.exchanges.base import ExchangeAdapter


class ASXAdapter(ExchangeAdapter):

    @property
    def exchange_name(self) -> str:
        return "Australian Securities Exchange (ASX)"

    @property
    def exchange_code(self) -> str:
        return "ASX"

    @property
    def clearing_house(self) -> str:
        return "ASX Clear (Futures)"

    def public_urls(self) -> dict:
        return {
            "product_list": "https://www.asx.com.au/markets/trade-our-derivatives-market",
            "daily_price": "https://www.asx.com.au/markets/trade-our-derivatives-market/derivatives-market-prices",
            "exchange_fees": "https://www.asx.com.au/about/fees",
        }
