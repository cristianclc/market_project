#orquestador, crea la el objeto de geckoclient, realiza la snapshopt, y lo guarda

from config.constants import RAW_PREFIX
from datetime import datetime
from pathlib import Path
from ingestion.api_client import CoinGeckoClient
from load_storage.local_storage import save_json
from load_storage.gcs_storage import upload_file



def main():
    api_connection = CoinGeckoClient() #se crea la clase que se conecta con la api
    snapshot = api_connection.get_market_snapshot() #método del snapshot del mercado


    cur_date = datetime.now()
    date_name = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S') #fecha actual para el nombre
    route_to_raw = Path.cwd() / "data" / "raw" #ruta para el raw
    route_to_raw.mkdir(parents=True, exist_ok=True) #crea la carpeta si no exite

    save_json(snapshot, route_to_raw / f'market_snapshot_{date_name}.json') #se guarda el json, se manda la lista materialzable y la dirección

    json_route = route_to_raw / f'market_snapshot_{date_name}.json' #convertimos la ruta en local de los json en una variable



    upload_file(json_route, f"{RAW_PREFIX}/year={cur_date.year}/month={cur_date.month:02d}/day={cur_date.day:02d}/{json_route.name}") #hacemos el upload en gcs, le pasamos la ruta del archivo y la ruta final en gcs
    
if __name__ == "__main__":
    main()
