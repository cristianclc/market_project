# objetivo tener información de coin-gecko
import requests
import config.constants


class CoinGeckoClient():
    
    def get_market_snapshot(
        self,
        url=config.constants.BASE_URL,
        endpoint=config.constants.MARKETS_ENDPOINT,
        currency=config.constants.DEFAULT_CURRENCY,
        per_page=config.constants.DEFAULT_PER_PAGE,
        order=config.constants.DEFAULT_ORDER,
        page=config.constants.DEFAULT_PAGES):
        
        
        params = {
        "vs_currency": currency,
        "per_page": per_page,
        "page": page,
        "order": order,
        }
        
        response = requests.get(f"{url}{endpoint}", params=params, timeout=300)
        
        response.raise_for_status()
        return response.json()
        