from google.cloud import pubsub_v1
import logging
import json
from concurrent.futures import TimeoutError

logger = logging.getLogger()
logger.setLevel(logging.INFO)
PROJECT_ID = "sdp-bnb"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/sdp-bnb/subscriptions/bnb-kitchen-topic-sub'
result = []


def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')
    decode_message = message.data.decode("utf-8")
    print(f'decode_message: {decode_message}')
    js = json.loads(decode_message)
    result.append(js)
    print('result')
    print(result)


def pull_notification(request):
    print("-------------------------------------------------------")
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result(timeout=2)
            print("-----ok1------")
            return "done"
        except TimeoutError:
            print("-----ok------")
            print(str(result))
            return (json.dumps(result), 200, headers)
