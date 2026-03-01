"""CME Group adapter (CME / CBOT / NYMEX / COMEX)."""

from market_search.exchanges.base import ExchangeAdapter


class CMEAdapter(ExchangeAdapter):

    @property
    def exchange_name(self) -> str:
        return "CME Group (CME/CBOT/NYMEX/COMEX)"

    @property
    def exchange_code(self) -> str:
        return "CME"

    @property
    def clearing_house(self) -> str:
        return "CME Clearing"

    def public_urls(self) -> dict:
        return {
            "product_list": "https://www.cmegroup.com/markets.html",
            "product_detail": "https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.html",
            "daily_price": "https://www.cmegroup.com/market-data/daily-bulletin.html",
            "contract_dates": "https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.contractSpecs.html",
            "margin_rates": "https://www.cmegroup.com/clearing/margins/outright-vol-scans.html",
            "exchange_fees": "https://www.cmegroup.com/company/clearing-fees.html",
        }
