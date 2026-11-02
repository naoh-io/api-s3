import base64
import binascii
import mimetypes

import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Entrada (json): el archivo viaja codificado en base64
    bucket = event['body']['bucket']
    directorio = event['body']['directorio'].strip('/')
    nombre_archivo = event['body']['nombre_archivo']
    contenido_base64 = event['body']['contenido_base64']
    # Proceso
    try:
        contenido = base64.b64decode(contenido_base64, validate=True)
    except (binascii.Error, ValueError):
        # Salida (json)
        return {'statusCode': 400, 'mensaje': 'contenido_base64 no es un base64 valido'}
    key = directorio + '/' + nombre_archivo
    content_type = mimetypes.guess_type(nombre_archivo)[0] or 'application/octet-stream'
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=contenido, ContentType=content_type)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            return {'statusCode': 404, 'mensaje': 'El bucket no existe', 'bucket': bucket}
        raise
    # Salida (json)
    return {
        'statusCode': 200,
        'mensaje': 'Archivo subido',
        'bucket': bucket,
        'key': key,
        'bytes': len(contenido)
    }
