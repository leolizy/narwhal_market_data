"""Hong Kong Exchanges (HKEX) adapter."""

from market_search.exchanges.base import ExchangeAdapter


class HKEXAdapter(ExchangeAdapter):

    @property
    def exchange_name(self) -> str:
        return "Hong Kong Exchanges (HKEX)"

    @property
    def exchange_code(self) -> str:
        return "HKEX"

    @property
    def clearing_house(self) -> str:
        return "HKEX Clearing (HKCC)"

    def public_urls(self) -> dict:
        return {
            "product_list": "https://www.hkex.com.hk/Products/Listed-Derivatives",
            "daily_price": "https://www.hkex.com.hk/Market-Data/Futures-and-Options-Prices",
            "margin_rates": "https://www.hkex.com.hk/Services/Clearing/Listed-Derivatives/Risk-Management/Margin",
            "exchange_fees": "https://www.hkex.com.hk/Services/Rules-and-Forms-and-Fees/Fees",
        }
