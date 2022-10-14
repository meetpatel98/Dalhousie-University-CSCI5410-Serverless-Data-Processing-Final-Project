import json
import re
import boto3
import pandas as pd
import simplejson as json
from decimal import Decimal
from google.cloud import storage

def tour(request):
    session = boto3.Session(
        aws_access_key_id='ASIA4CLIBNVAWRQWPCO2',
        aws_secret_access_key='rRh9GBJiDgucsLw4qbs9oPfyxjYlHG66ve/8Vpsw',
        aws_session_token='FwoGZXIvYXdzED4aDKYu/lwPdZFDENOzEyLAAXQ+jNTjQJMnZ3sxB3fy7qHyFhDWBchHy9QfZOzENiEAQtAd8U1R1fL2GJHySoPK3gIH/9rj7xI9RYcJlF02qwuaCej0ljMAlHb3uGi5mrpD2sIkW9c2vpY6pUwgGKdG4r4Rfom4S9iWGpvGx5l08tANXbfvmLeSWyrQ+jgUB20DFA0gehuse5ADDcZiZsVa9aIpfTJm/0KY7InoXQ2x+kAdoslyVynBfzJeuS41hofl2NtWl3I7n+yCzhZUJBvyOijjzO+WBjItTzo3MJl8yDLbaMAXG2/WJ7WOG1ZHrf9LfQOHDbXN0xircwExL6Xc9a1GMbuF',
        region_name='us-east-1'
    )
    print('session valid', session)

    storage_client = storage.Client()
    bucket = storage_client.bucket('serverless-project-visualization')
    print('got bucket')
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('tour')
    
    response = table.scan()
    print('db res: ', response)
    result = response['Items']
    print('result: ', result)
    df = pd.DataFrame(result)
    
    bucket.blob('tour.csv').upload_from_string(df.to_csv(index=False), 'text/csv')

    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result,use_decimal=True),
        'message': 'Tour'
    }