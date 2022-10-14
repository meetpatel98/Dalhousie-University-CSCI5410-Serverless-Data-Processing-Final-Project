import json
import logging
import requests
import time
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    request_path = event['requestContext']['http']['path']
    body = {}
    if 'body' in event and event['body']:
        req_body = json.loads(event['body'])
        if request_path == '/login_success':
            logger.info("/login_success")
            if req_body['status'] == "1":
                logger.info(
                    f"Login status: success | Customer id: {customer_id}")
            else:
                logger.info(
                    f"Login status: success | Customer id: {customer_id}")
            return build_response(200)
        elif request_path == '/book_room':
            rid = str(uuid.uuid1())
            url = "https://vgjfo3gxbacdua7gokt7qfkjle0xobth.lambda-url.us-east-1.on.aws/book_room"
            req_body['request_id'] = rid
            payload = json.dumps(req_body)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            time.sleep(2)

            # pull message from hotel topic
            success = False
            ctr = 5
            resjs = []
            while ctr >= 0 and success == False:
                url = "https://us-central1-sdp-bnb.cloudfunctions.net/pullHotelMessage"
                payload = {}
                headers = {}
                response = requests.request(
                    "GET", url, headers=headers, data=payload)
                if response.status_code == 500:
                    ctr -= 1
                    continue
                else:
                    success = True
                    resjs = json.loads(response.text)

            if len(resjs) > 0:
                for res in resjs:
                    if res['request_id'] == rid and res['status'] == "Complete":
                        return build_response(200)

    return build_response(404, 'Not Found')


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
    }
    if body:
        response['body'] = body
    return response
