import json
import logging
from google.cloud import pubsub_v1

PROJECT_ID = "sdp-bnb"

publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/sdp-bnb/topics/bnb-kitchen-topic'


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def post_notification(request):
    logger.info(request)
    body = request.data
    message_bytes = body
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()
        return build_response(200, None)
    except Exception as e:
        print(e)
        return build_response(500, None)


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body:
        response['body'] = body
    return response
