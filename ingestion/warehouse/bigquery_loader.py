#cargamos los json de google cloud storage a bigquery

from google.cloud import bigquery

client = bigquery.Client()

def bigquery_load_from_gcs(uri: str, table_id:str): #uri es el enlace del ndjson en gcs, table_id es la tabla donde se va a subiren bigquery
    # table_id = "your-project.your_dataset.your_table_name
    job_config = bigquery.LoadJobConfig( 
        autodetect=True, #schema del json
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND #sirve para que la tabla no se reescriba, si no que se agregue
    )

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)

    return load_job.result()



