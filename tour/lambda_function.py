import json
import logging
from routes import GET_TOURS_ROUTE, BOOK_TOUR_ROUTE, ROOT, GET_TOUR_BOOKINGS
from services import get_tours, book_tour, get_tour_bookings

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    request_path = event['requestContext']['http']['path']
    body = {}
    if 'body' in event and event['body']:
        body = json.loads(event['body'])
    if request_path == GET_TOURS_ROUTE:
        return build_response(200, get_tours(logger, body['num_of_days']))
    elif request_path == BOOK_TOUR_ROUTE:
        request_id = body['request_id'] if 'request_id' in body else ''
        return build_response(201, book_tour(logger, body['tour_id'], body['customer_id'], body['booking_id'], body['quantity'], request_id))
    elif request_path == GET_TOUR_BOOKINGS:
        return build_response(201, get_tour_bookings(logger, body['customer_id']))
    elif request_path == ROOT:
        return build_response(200, "Tour Service is alive!")
    else:
        return build_response(404, 'Not Found')


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code
    }
    if body:
        response['body'] = body
    return response
