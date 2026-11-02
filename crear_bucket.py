import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Entrada (json)
    bucket = event['body']['bucket']
    # Proceso
    s3 = boto3.client('s3')
    try:
        # us-east-1 no necesita LocationConstraint
        s3.create_bucket(Bucket=bucket)
    except ClientError as e:
        codigo = e.response['Error']['Code']
        if codigo in ('BucketAlreadyOwnedByYou', 'BucketAlreadyExists'):
            # Salida (json)
            return {'statusCode': 409, 'mensaje': 'El bucket ya existe', 'bucket': bucket}
        if codigo == 'InvalidBucketName':
            return {'statusCode': 400, 'mensaje': 'Nombre de bucket invalido', 'bucket': bucket}
        raise
    # Salida (json)
    return {'statusCode': 200, 'mensaje': 'Bucket creado', 'bucket': bucket}
