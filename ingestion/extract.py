#orquestador, crea la el objeto de geckoclient, realiza la snapshopt, y lo guarda

from config.constants import RAW_PREFIX, STAGED_PREFIX, PROJECT_ID, GCS_BUCKET
from datetime import datetime
from pathlib import Path
from ingestion.api_client import CoinGeckoClient
from load_storage.local_storage import save_json
from load_storage.gcs_storage import upload_file
from transform.json_to_ndjson import ndjson_transform
from ingestion.warehouse.bigquery_loader import bigquery_load_from_gcs


def main():
    api_connection = CoinGeckoClient() #se crea la clase que se conecta con la api
    snapshot = api_connection.get_market_snapshot() #método del snapshot del mercado


    cur_date = datetime.now()
    date_name = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S') #fecha actual para el nombre

    route_to_raw = Path.cwd() / "data" / "raw" #ruta para el raw
    route_to_raw.mkdir(parents=True, exist_ok=True) #crea la carpeta si no exite

    route_to_staged = Path.cwd() / "data" / "staged" #ruta para el staged
    route_to_staged.mkdir(parents=True, exist_ok=True) #crea la carpeta si no exite

    save_json(snapshot, route_to_raw / f'market_snapshot_{date_name}.json') #se guarda el json, se manda la lista materialzable y la dirección
    json_route = route_to_raw / f'market_snapshot_{date_name}.json' #convertimos la ruta en local de los json en una variable

    ndjson_transform(json_route, route_to_staged / f'market_snapshot_{date_name}.ndjson', cur_date) #transformamos el json que acabamos de crear a ndjson
    ndjson_route = route_to_staged / f'market_snapshot_{date_name}.ndjson'

    upload_file(json_route, f"{RAW_PREFIX}/year={cur_date.year}/month={cur_date.month:02d}/day={cur_date.day:02d}/{json_route.name}") #hacemos el upload en gcs, le pasamos la ruta del archivo y la ruta final en gcs
    upload_file(ndjson_route, f"{STAGED_PREFIX}/year={cur_date.year}/month={cur_date.month:02d}/day={cur_date.day:02d}/{ndjson_route.name}") #uplead al staged


    # CARGA A BIGQUERY
    table_name = f"{PROJECT_ID}.crypto_raw.market_snapshot"

    bigquery_load_from_gcs(f"gs://{GCS_BUCKET}/{STAGED_PREFIX}/year={cur_date.year}/month={cur_date.month:02d}/day={cur_date.day:02d}/{ndjson_route.name}", table_name) #se carga a bigquery
    
if __name__ == "__main__":
    main()
