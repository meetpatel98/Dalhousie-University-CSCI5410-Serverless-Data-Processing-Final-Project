import json
import logging
from routes import GET_AVAILABLE_ROOMS_ROUTE, BOOK_ROOM_ROUTE, GET_BOOKING_DETAILS, POST_HOTEL_FEEDBACK, GET_FEEDBACKS
from services import get_available_rooms_service, booking_hotel, get_booking_details, post_hotel_feedback, get_feedbacks

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    request_path = event['requestContext']['http']['path']
    body = {}
    if 'body' in event and event['body']:
        body = json.loads(event['body'])
    if request_path == GET_AVAILABLE_ROOMS_ROUTE:
        return build_response(200, get_available_rooms_service(logger, body['checkin_date'], body['checkout_date']))
    elif request_path == BOOK_ROOM_ROUTE:
        return build_response(201, booking_hotel(logger, body['room_id'], body['customer_id'], body['checkin_date'], body['checkout_date']))
    elif request_path == GET_BOOKING_DETAILS:
        return build_response(200, get_booking_details(logger, body['customer_id']))
    elif request_path == POST_HOTEL_FEEDBACK:
        return build_response(200, post_hotel_feedback(logger, body['booking_id'], body['customer_id'], body['feedback']))
    elif request_path == GET_FEEDBACKS:
        return build_response(200, get_feedbacks(logger))
    else:
        return build_response(404, 'Not Found')


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
    }
    if body:
        response['body'] = body
    return response
