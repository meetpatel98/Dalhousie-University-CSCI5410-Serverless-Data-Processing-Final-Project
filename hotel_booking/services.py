from datetime import datetime
import uuid
from dynamodb import DynamoDB
from dynamo_collections import ROOM, BOOKING_DETAILS, HOTEL_FEEDBACK
from handle_notification import post_notification
import json
import requests


sentiment_url = "https://us-central1-serverless-project-164d7.cloudfunctions.net/SentimentAnalysis"


def get_available_rooms_service(logger, check_in, check_out):
    dynamo = DynamoDB()
    rooms = dynamo.get_all_records(ROOM)
    logger.info(rooms)
    bookings = dynamo.get_all_records(BOOKING_DETAILS)
    available_rooms = []
    check_in_v2 = datetime.strptime(check_in, "%Y/%m/%d")
    check_out_v2 = datetime.strptime(check_out, "%Y/%m/%d")

    for room in rooms:
        common_bookings = [booking for booking in bookings if room['id'] ==
                           booking['room_id'] and
                           not (check_in_v2 >= datetime.strptime(booking['checkout_date'], "%Y/%m/%d") or
                                (check_in_v2 < datetime.strptime(booking['checkin_date'],
                                                                 "%Y/%m/%d") and check_out_v2 <= datetime.strptime(
                                    booking['checkin_date'], "%Y/%m/%d")))]
        if not common_bookings:
            available_rooms.append(room)
    logger.info(available_rooms)
    return None if not available_rooms else available_rooms


def booking_hotel(logger, room_id, customer_id, checkin_date, checkout_date):
    dynamo = DynamoDB()
    book_room_details = dynamo.get_record(ROOM, {'id': room_id})
    logger.info(book_room_details)
    d1 = datetime.strptime(checkin_date, "%Y/%m/%d")
    d2 = datetime.strptime(checkout_date, "%Y/%m/%d")
    td = d2-d1
    logger.info(td)
    days = td.days
    logger.info(days)
    total_cost = book_room_details[0]['cost_per_day'] * days
    data = {
        'id': str(uuid.uuid1()),
        'room_id': room_id,
        'customer_id': customer_id,
        'checkin_date': checkin_date,
        'checkout_date': checkout_date,
        'total_cost': total_cost,
        'timestamp': str(datetime.now())
    }
    dynamo.insert(BOOKING_DETAILS, data)
    post_notification({
        "customer_id": customer_id,
        "message": "Room booked | Check-in date: {} | Check-out date: {} | Total Cost: ${} | Booking date: {}".format(
            d1.strftime("%B %d, %Y"), d2.strftime("%B %d, %Y"), total_cost, str(datetime.now().strftime("%B %d, %Y at %H:%M"))
        )
    })


def get_booking_details(logger, customer_id):
    dynamo = DynamoDB()
    bookings = dynamo.get_all_records(BOOKING_DETAILS)
    logger.info(bookings)
    customer_booking_details = [
        booking for booking in bookings if booking['customer_id'] == customer_id]
    logger.info(customer_booking_details)
    return customer_booking_details


def post_hotel_feedback(logger, booking_id, customer_id, feedback):
    dynamo = DynamoDB()
    feedback_sentiment = get_sentiment(feedback)
    data = {
        'booking_id': booking_id,
        'customer_id': customer_id,
        'feedback': feedback,
        'feedback_polarity': feedback_sentiment.get("polarity"),
        'feedback_sentimentscore': str(feedback_sentiment.get("sentimentscore"))
    }
    logger.info(data)
    dynamo.insert(HOTEL_FEEDBACK, data)
    post_notification({
        "customer_id": customer_id,
        "message": "Feedback posted for booking: {}".format(booking_id)
    })


def get_feedbacks(logger):
    dynamo = DynamoDB()
    feedbacks = dynamo.get_all_records(HOTEL_FEEDBACK)
    return feedbacks


def get_sentiment(feedback):
    payload = json.dumps({
      "text": feedback
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjYzMWZhZTliNTk0MGEyZDFmYmZmYjAwNDAzZDRjZjgwYTIxYmUwNGUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNjE4MTA0NzA4MDU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zMm42ZGdxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNjE4MTA0NzA4MDU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zMm42ZGdxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA1NDY4NDkyMzU3NzI5MDY5OTUwIiwiZW1haWwiOiJtdWt1bmRzaGFybWExOTk1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiWEpqSGFvRUttU2UtdjdlOWJGNU85QSIsImlhdCI6MTY1ODI3NzY1MSwiZXhwIjoxNjU4MjgxMjUxLCJqdGkiOiJjZWZlMDZhMjUxNDI2ZmFjMGI5Nzk4ZWE4OWRlMDUzN2IwNWFjMmZiIn0.CUSSx2_AARuRhrx87eOSam0ov84wWmHMNoUJ8b2OA4kj2f6xRl5oFxVkxDrAF8R3niWAvo-Ey6VLSNkExAf_WvZSV7bt-V_2u9W4Vy4lrZlGyCSRF-Pcl6i5cCzdmOxQ3hNRvjuLOUT9RGI6NC7r8it8Z6gNVEwHzZCsUTfxJZQvx0-6KwZ01x4_xWWuVvUoktdM3BM6vFH9LepVZ8lH5f5aKX_jtBW98DPma-F5GVPRFo3HS6cMOk9C0eaTNgGQ3mvr0gfIPnntN52ax-4nE3qWoJmR2HQPUQR4Bkv6lLZcEepOUMNyXW9aezJnCsWDJw0-FF4_PCRxwy9m0se_Yw'
    }
    response = requests.request("POST", sentiment_url, headers=headers, data=payload)
    return json.loads(response.text)
