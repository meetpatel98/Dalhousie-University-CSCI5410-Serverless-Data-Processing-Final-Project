import json
import re
import boto3
import pandas as pd
import simplejson as json
from decimal import Decimal
from google.cloud import storage

def booking_details(request):
    session = boto3.Session(
        aws_access_key_id='ASIA4CLIBNVA7IUB3RNB',
        aws_secret_access_key='KccgHoUj04ktP0m0GaGq97rR+6RR9bI/fEqAsUjQ',
        aws_session_token='FwoGZXIvYXdzEM7//////////wEaDAfeXXI+N7Zr7mra+iLAAdyjanOvtLmrf7oW0BnQienBwGQifORsu8SVIeG09tApaiE5X0g4Vwr8u3qpToVuhdMS6jTtOG3iej1bRD5YFkfYVaTIyMi5Ydz+x9rR14zND3p9F4uv1wIlyCTwvN+/9Gf3GvkwHJ+ex0oJQzabURkBM1P68EJ47EeO+FASzDGjorpyU+gCdxIXS/W4e+XiQuavEoBlxTmIgEtzR/2TXtuaapn16zhZCUL8Qk98BM2oz0aBUsKDUWGeRBXaZf9Rhii5+9aWBjItyyaXRrwMNbaGX4yVoWSRiZ/sSb/T6TUc8SbFSQWvU2vPNVzJTRwyF3pnyFAB',
        region_name='us-east-1'
    )
    print('session valid', session)

    storage_client = storage.Client()
    bucket = storage_client.bucket('serverless-project-visualization')
    print('got bucket')
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('booking_details')
    
    response = table.scan()
    print('db res: ', response)
    result = response['Items']
    print('result: ', result)
    df = pd.DataFrame(result)
    
    bucket.blob('booking_details.csv').upload_from_string(df.to_csv(index=False), 'text/csv')

    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result,use_decimal=True),
        'message': 'Booking Details'
    }