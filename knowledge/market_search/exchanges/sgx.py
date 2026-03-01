"""Singapore Exchange (SGX) adapter."""

from market_search.exchanges.base import ExchangeAdapter


class SGXAdapter(ExchangeAdapter):

    @property
    def exchange_name(self) -> str:
        return "Singapore Exchange (SGX)"

    @property
    def exchange_code(self) -> str:
        return "SGX"

    @property
    def clearing_house(self) -> str:
        return "SGX Derivatives Clearing"

    def public_urls(self) -> dict:
        return {
            "product_list": "https://www.sgx.com/derivatives/products",
            "daily_price": "https://www.sgx.com/derivatives/market-prices",
            "margin_rates": "https://www.sgx.com/derivatives/risk-management",
            "exchange_fees": "https://www.sgx.com/derivatives/trading/fees",
        }
