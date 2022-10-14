import boto3
import json
from datetime import datetime, timedelta
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    request_path = event['requestContext']['http']['path']

    log_group = '/aws/lambda/'
    filter_string = ''

    if request_path == '/hotel-stats':
        logger.info("here!!")
        filter_string = 'book_room'
        log_group = log_group+'hotelBooking'
    elif request_path == '/meal-stats':
        filter_string = 'order_meal'
        log_group = log_group+'kitchenService'
    elif request_path == '/tour-stats':
        filter_string = 'book_tour'
        log_group = log_group+'tourService'
    elif request_path == '/login-stats':
        filter_string = 'login_success'
        log_group = log_group+'customerService'
    elif request_path == '/login-stats-v2':
        filter_string = 'Login status'
        log_group = log_group+'customerService'
        return build_response(200, fetch_reporting_datav2(filter_string, log_group))
    elif request_path == '/hotel-stats-v2':
        filter_string = 'Room booking status'
        log_group = log_group+'hotelBooking'
        return build_response(200, fetch_reporting_datav2(filter_string, log_group))
    elif request_path == '/meal-stats-v2':
        filter_string = 'Meal order status'
        log_group = log_group+'kitchenService'
        return build_response(200, fetch_reporting_datav2(filter_string, log_group))
    elif request_path == '/tour-stats-v2':
        filter_string = 'Tour booking status'
        log_group = log_group+'tourService'
        return build_response(200, fetch_reporting_datav2(filter_string, log_group))
    else:
        return build_response(404, 'Not Found')

    return build_response(200, fetch_reporting_data(filter_string, log_group))


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code
    }
    if body:
        response['body'] = body
    return response


def fetch_reporting_data(filter_string, log_group):
    client = boto3.client('logs')
    query = f"fields @timestamp, @message | filter @message like /{filter_string}/ and @message  like /INFO/ | stats count() by bin(30s)"
    logger.info(query)
    logger.info(log_group)
    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=int((datetime.today() - timedelta(hours=24)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        queryString=query,
    )
    query_id = start_query_response['queryId']
    response = None
    while response == None or response['status'] == 'Running':
        print('Waiting for query to complete ...')
        time.sleep(1)
        response = client.get_query_results(
            queryId=query_id
        )
    return response


def fetch_reporting_datav2(filter_string, log_group):
    client = boto3.client('logs')
    query = f"fields @timestamp, @message | filter @message like /{filter_string}/ and @message  like /INFO/"
    logger.info(query)
    logger.info(log_group)
    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=int((datetime.today() - timedelta(hours=24)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        queryString=query,
    )

    query_id = start_query_response['queryId']
    response = None
    while response == None or response['status'] == 'Running':
        print('Waiting for query to complete ...')
        time.sleep(1)
        response = client.get_query_results(
            queryId=query_id
        )
    # return response
    items = response['results']
    res = ''
    for item in items:
        for keyval in item:
            if keyval['field'] == '@message':
                res += keyval['value']
    return res
