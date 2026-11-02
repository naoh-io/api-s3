import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Entrada (json)
    bucket = event['body']['bucket']
    directorio = event['body']['directorio'].strip('/')
    # Proceso
    s3 = boto3.client('s3')
    try:
        # En S3 un "directorio" es un objeto vacio cuya clave termina en "/"
        s3.put_object(Bucket=bucket, Key=directorio + '/')
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            # Salida (json)
            return {'statusCode': 404, 'mensaje': 'El bucket no existe', 'bucket': bucket}
        raise
    # Salida (json)
    return {
        'statusCode': 200,
        'mensaje': 'Directorio creado',
        'bucket': bucket,
        'directorio': directorio + '/'
    }
