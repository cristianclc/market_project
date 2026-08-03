#cargamos los json de google cloud storage a bigquery

from google.cloud import bigquery

client = bigquery.Client()

job_config = bigquery.LoadJobConfig( #schema del json
    schema=[
        bigquery.SchemaField
    ],
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
)

def biquery_load_from_gcs(uri):
    pass

