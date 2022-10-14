import json
import re
import boto3
import pandas as pd
import simplejson as json
from decimal import Decimal
from google.cloud import storage

def tour_booking(request):
    session = boto3.Session(
        aws_access_key_id='ASIA4CLIBNVARVQUX4ET',
        aws_secret_access_key='3phVlt9dwvt5Tte2fXFUfIh+7HhwDErapJsNkxTZ',
        aws_session_token='FwoGZXIvYXdzEN7//////////wEaDLNqlNwREEfJ8yridCLAAasEDAlGkTJzIGQMHdOSCh2/lC5b9pRMyHIdEvZ68Apq68fH5+Yo8VMz7PABWVaynj/BTqDAcy9VKi2r9I7OiaiqtFSpdbzB229PHySqBTrNOhLzeY+OcfFCgVYxn5Fp2mXba7ftOOCNbEzl0qw2nG/IGgKacPKJh2QEPWrTJSnQHs3KgJVIW/ZW5DHS3N9ivR1REGmZYWjkUA9w9YMQ/zrQ4LoI7tFVJ9Hp6FIzffs0PZxZqyLwzN9NwOGVRPI1gyiZ0dqWBjItMtjl09V62Rbza/53Zkj1+cwItc3mChxLqKMjii+08QDu3iCc+Sv4tgP4D8WH',
        region_name='us-east-1'
    )
    print('session valid', session)

    storage_client = storage.Client()
    bucket = storage_client.bucket('serverless-project-visualization')
    print('got bucket')
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('tour_booking')
    
    response = table.scan()
    print('db res: ', response)
    result = response['Items']
    print('result: ', result)
    df = pd.DataFrame(result)
    
    bucket.blob('tour_booking.csv').upload_from_string(df.to_csv(index=False), 'text/csv')

    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result,use_decimal=True),
        'message': 'Tour Booking'
    }