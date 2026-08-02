# objetivo tener información de coin-gecko
import requests
import config.constants


class CoinGeckoClient():
    
    def get_market_snapshot(
        self,
        url=config.constants.BASE_URL, #api url
        endpoint=config.constants.MARKETS_ENDPOINT, #endpoint
        currency=config.constants.DEFAULT_CURRENCY, #moneda
        per_page=config.constants.DEFAULT_PER_PAGE, #cuantas por pagina
        order=config.constants.DEFAULT_ORDER, #orden en el que se muestran
        page=config.constants.DEFAULT_PAGES): #cuantas paginas
        
        
        params = {
        "vs_currency": currency,
        "per_page": per_page,
        "page": page,
        "order": order,
        }
        
        response = requests.get(f"{url}{endpoint}", params=params, timeout=300)
        
        response.raise_for_status()
        return response.json()
        