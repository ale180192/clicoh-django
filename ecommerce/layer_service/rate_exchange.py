from decimal import Decimal
import requests
import logging

logger = logging.getLogger(__name__)

class RateExchange():
    # TODO(alex): implement cache logic.
    URL = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"

    @classmethod
    def fetch_rate_usd_blue(cls) -> float:
        """
        Gets the exchange rate from third party provider.
        """
        response = requests.get(cls.URL)

        if response.status_code != 200:
            logger.error("Could not get currency exchange ")
            return None

        rates = response.json()

        for item in rates:
            if item.get("casa", {}).get("nombre") == "Dolar Blue":
                integer_part, decimal_part = item["casa"]["compra"].split(",")
                return 1/Decimal(f"{integer_part}.{decimal_part}")

        return None
