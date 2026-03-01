"""Abstract base class for exchange adapters."""

from abc import ABC, abstractmethod


# Ordered by priority
DATA_CATEGORIES = [
    "product_list",
    "product_detail",
    "daily_price",
    "contract_dates",
    "margin_rates",
    "exchange_fees",
]


class ExchangeAdapter(ABC):
    """Base class that every exchange adapter must implement."""

    @property
    @abstractmethod
    def exchange_name(self) -> str:
        """Human-readable exchange name."""

    @property
    @abstractmethod
    def exchange_code(self) -> str:
        """Short code, e.g. 'CME', 'ICE'."""

    @property
    @abstractmethod
    def clearing_house(self) -> str:
        """Name of the clearing house."""

    @abstractmethod
    def public_urls(self) -> dict:
        """Return dict mapping data category to public URL."""

    def data_categories(self) -> list:
        """Return the data categories this exchange provides (ordered by priority)."""
        return [c for c in DATA_CATEGORIES if c in self.public_urls()]

    def summary(self) -> dict:
        """Return a summary dict suitable for JSON output."""
        return {
            "exchange_code": self.exchange_code,
            "exchange_name": self.exchange_name,
            "clearing_house": self.clearing_house,
            "data_categories": self.data_categories(),
            "public_urls": self.public_urls(),
        }
