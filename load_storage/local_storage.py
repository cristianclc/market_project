#objetivo guardar los json de las monedas
import json


def save_json(data, output_file):
    
    with output_file.open("w", encoding="utf-8") as json_route:
        json.dump(data, json_route, indent=4, ensure_ascii=False)