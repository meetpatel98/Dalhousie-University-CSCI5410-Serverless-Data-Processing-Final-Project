from google.cloud import pubsub_v1
import logging
import json
from concurrent.futures import TimeoutError

logger = logging.getLogger()
logger.setLevel(logging.INFO)
PROJECT_ID = "sdp-bnb"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/sdp-bnb/subscriptions/bnb-notification-topic-sub'
result = []


def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')
    decode_message = message.data.decode("utf-8")
    print(f'decode_message: {decode_message}')
    js = json.loads(decode_message)
    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")

    result.append(js)
    print('result')
    print(result)


def pull_notification(request):
    print("-------------------------------------------------------")
    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result(timeout=5)
            print("-----ok1------")
            return "done"
        except TimeoutError:
            print("-----ok------")
            print(str(result))
            return json.dumps(result), 200, {'Content-Type': 'application/json'}
            streaming_pull_future.cancel()
            streaming_pull_future.result()
