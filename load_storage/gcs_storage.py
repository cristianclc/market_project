#se encarga de subir archivos en local al gcs

from google.cloud import storage
from config.constants import GCS_BUCKET #nombre del bucket
from pathlib import Path

storage_client = storage.Client() #conectamos el cliente, la referencia el proyecto al tiene el json del service accout

#set GOOGLE_APPLICATION_CREDENTIALS=KEY_PATH esta es la variable de entorno para que la clase client reconozca la service account

def upload_file(source_file_path: Path, destination_path: str):
    #source_file es el archivo que vamos a subir
    #destination_path es como una especia de dirección en el bucket para nuestro archivo

    if not source_file_path.exists(): #exists es eun métodod de la clse path para verificar que exista
        raise FileNotFoundError()

    bucket = storage_client.bucket(GCS_BUCKET) #le damos la referencia a la bucket
    blob = bucket.blob(destination_path) #le damos la referencia del blob de nuestra bucket

    blob.upload_from_filename(source_file_path) #cargamos desde el archivo en local al bucket

    return destination_path