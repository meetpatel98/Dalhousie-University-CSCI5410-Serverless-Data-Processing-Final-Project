import json
import logging
from routes import GET_MEALS_ROUTE, ORDER_MEAL_ROUTE, GET_MEAL_BOOKINGS
from services import get_meals, order_meal, get_meal_bookings

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    request_path = event['requestContext']['http']['path']
    body = {}
    if 'body' in event and event['body']:
        body = json.loads(event['body'])
    if request_path == GET_MEALS_ROUTE:
        return build_response(200, get_meals(logger))
    elif request_path == ORDER_MEAL_ROUTE:
        request_id = body['request_id'] if 'request_id' in body else ''
        return build_response(201, order_meal(logger, body['meal_id'], body['customer_id'], body['booking_id'], body['quantity'], request_id))
    elif request_path == GET_MEAL_BOOKINGS:
        return build_response(201, get_meal_bookings(logger, body['customer_id']))
    else:
        return build_response(404, 'Not Found')


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code
    }
    if body:
        response['body'] = body
    return response
