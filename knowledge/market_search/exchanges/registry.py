"""Registry that maps exchange codes to adapter classes."""

from market_search.exchanges.cme import CMEAdapter
from market_search.exchanges.ice import ICEAdapter
from market_search.exchanges.eurex import EurexAdapter
from market_search.exchanges.lme import LMEAdapter
from market_search.exchanges.sgx import SGXAdapter
from market_search.exchanges.asx import ASXAdapter
from market_search.exchanges.hkex import HKEXAdapter


_REGISTRY: dict = {
    "CME": CMEAdapter,
    "ICE": ICEAdapter,
    "EUREX": EurexAdapter,
    "LME": LMEAdapter,
    "SGX": SGXAdapter,
    "ASX": ASXAdapter,
    "HKEX": HKEXAdapter,
}


def get_adapter(code: str):
    """Return an instantiated adapter for the given exchange code.

    Raises KeyError if the code is not registered.
    """
    code_upper = code.upper()
    if code_upper not in _REGISTRY:
        raise KeyError(
            f"Unknown exchange code '{code}'. "
            f"Available: {', '.join(sorted(_REGISTRY))}"
        )
    return _REGISTRY[code_upper]()


def list_exchanges() -> list:
    """Return a list of summary dicts for every registered exchange."""
    return [cls().summary() for cls in _REGISTRY.values()]
