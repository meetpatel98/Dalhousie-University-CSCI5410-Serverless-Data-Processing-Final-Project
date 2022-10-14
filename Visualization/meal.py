import json
import re
import boto3
import pandas as pd
import simplejson as json
from decimal import Decimal
from google.cloud import storage

def meal(request):
    session = boto3.Session(
        aws_access_key_id='ASIA4CLIBNVA75XEWFQF',
        aws_secret_access_key='1Q4NgwheUovp9+gL4CpbVMib7uGkm39sKMu5ychq',
        aws_session_token='FwoGZXIvYXdzECsaDC1ogWxTbDr1H0J/3CLAAafi/VW7XEeEEXmPxDlnalDN7O1+txQiErV28skcW1kmDFOnLljo44hMrx8uQ/ubOG9C5ZAsZDs0t9FzcN6W98u3gaufkigMLRhYa6625sn4ffKjDlIt3dQ8ths7qNOBEf8PeH+8MEABv2uWGpywOLVYmCUFSbNtXxCTI/Ezjrub8oig9H6f5aMDQhyrg9+qqY/cDH/AuySWr2DCMjEWV4FaTMf2wUVG8dlY6q4bKO/puN1g4dPnVurfqqOQpIrQeijNxuuWBjItdIzUmjSyWV6CYV3XFyoJ5/AhxihdzF6Xzdfh0o0RQ3EZM+b5vGpeqB66uvTn',
        region_name='us-east-1'
    )
    print('session valid', session)

    storage_client = storage.Client()
    bucket = storage_client.bucket('serverless-project-visualization')
    print('got bucket')
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('meal')
    
    response = table.scan()
    print('db res: ', response)
    result = response['Items']
    print('result: ', result)
    df = pd.DataFrame(result)
    
    bucket.blob('meal.csv').upload_from_string(df.to_csv(index=False), 'text/csv')

    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result,use_decimal=True),
        'message': 'Meal'
    }