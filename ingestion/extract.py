#orquestador, crea la el objeto de geckoclient, realiza la snapshopt, y lo guarda

from datetime import datetime
from pathlib import Path
from ingestion.api_client import CoinGeckoClient
from storage.local_storage import save_json


def main():
    api_connection = CoinGeckoClient() #se crea la clase que se conecta con la api
    snapshot = api_connection.get_market_snapshot() #método del snapshot del mercado


    cur_date = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S') #fecha actual para el nombre
    route_to_raw = Path.cwd() / "data" / "raw" #ruta para el raw
    route_to_raw.mkdir(parents=True, exist_ok=True) #crea la carpeta si no exite

    save_json(snapshot, route_to_raw / f'market_snapshot_{cur_date}.json') #se guarda el json, se manda la lista materialzable y la dirección
    
if __name__ == "__main__":
    main()
