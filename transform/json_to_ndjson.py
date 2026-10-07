#convierte los archivos json y los transforma ndjson

import json
from pathlib import Path

def ndjson_transform(json_file: Path, staged_file:Path, cur_date):

    with json_file.open("r", encoding='utf-8') as file:
        data = json.load(file) #carga el json completo el archivo en local

    with staged_file.open("w", encoding="utf-8") as staged_file:
        for coin in data: #iteramos sobre el json completo, cada iteración representa una moneda (diccionario)
            coin['snapshot_date'] = cur_date.strftime('%Y-%m-%d') #agregamos la fecha
            json_line = json.dumps(coin) #convierte el diccionario de cada moneda en un objeto estilo json y retorna el string
            staged_file.write(json_line) #escribimos en el archivo el string json
            staged_file.write("\n") #salto de linea