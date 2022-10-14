from datetime import datetime
import uuid
from dynamodb import DynamoDB
from dynamo_collections import TOUR, TOUR_BOOKING
from handle_notification import post_notification
import requests
import json


tour_rec_url = "https://us-central1-serverless-assignment4-355813.cloudfunctions.net/similarHotels"


def get_tours(logger, num_of_days):
    dynamo = DynamoDB()
    tour_type = get_tour_recommendation(num_of_days)
    print("Rec tour type: {}".format(tour_type))
    tours = dynamo.get_all_records(TOUR)
    rec_tours = [tour for tour in tours if tour['tour_type'] == int(tour_type)]
    logger.info(rec_tours)
    return None if not rec_tours else rec_tours


def book_tour(logger, tour_id, customer_id, booking_id, quantity, request_id):
    try:
        dynamo = DynamoDB()
        tour = dynamo.get_record(TOUR, {'id': tour_id})
        logger.info(tour)
        total_cost = int(tour[0]['cost']) * int(quantity)
        logger.info(total_cost)
        data = {
            'id': str(uuid.uuid1()),
            'tour_id': tour_id,
            'customer_id': customer_id,
            'booking_id': booking_id,
            'quantity': quantity,
            'total_cost': total_cost,
            'time_stamp': str(datetime.now())
        }
        dynamo.insert(TOUR_BOOKING, data)
        post_notification({
            "customer_id": customer_id,
            "message": "Tour booked for booking {}| Quantity: {} | Total Cost: ${} | Tour Booking date: {}".format(
                booking_id, quantity, total_cost, str(
                    datetime.now().strftime("%B %d, %Y at %H:%M"))
            )
        })
        url = "https://us-central1-sdp-bnb.cloudfunctions.net/pushTourMessage"
        payload = json.dumps({
            "request_id": request_id,
            "status": "Complete"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        requests.request("POST", url, headers=headers, data=payload)
        logger.info(
            f"Tour booking status: success | Customer id: {customer_id}")
    except:
        url = "https://us-central1-sdp-bnb.cloudfunctions.net/pushTourMessage"
        payload = json.dumps({
            "request_id": request_id,
            "status": "Failed"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        requests.request("POST", url, headers=headers, data=payload)
        logger.info(
            f"Tour booking status: failed | Customer id: {customer_id}")


def get_tour_bookings(logger, customer_id):
    dynamo = DynamoDB()
    bookings = dynamo.get_all_records(TOUR_BOOKING)
    tours = dynamo.get_all_records(TOUR)
    tour_details = {tour['id']: [tour['tour_name'],
                                 tour['num_of_days']] for tour in tours}
    customer_tour_booking_details = []
    for booking in bookings:
        if booking['customer_id'] == customer_id:
            booking['tour_name'] = tour_details.get(booking.get('tour_id'))[0]
            booking['num_of_days'] = tour_details.get(
                booking.get('tour_id'))[1]
            customer_tour_booking_details.append(booking)
    return customer_tour_booking_details


def get_tour_recommendation(num_of_days):
    payload = json.dumps({
        "days": str(num_of_days)
    })
    print(payload)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjYzMWZhZTliNTk0MGEyZDFmYmZmYjAwNDAzZDRjZjgwYTIxYmUwNGUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNjE4MTA0NzA4MDU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zMm42ZGdxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNjE4MTA0NzA4MDU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zMm42ZGdxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA1NDY4NDkyMzU3NzI5MDY5OTUwIiwiZW1haWwiOiJtdWt1bmRzaGFybWExOTk1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiWEpqSGFvRUttU2UtdjdlOWJGNU85QSIsImlhdCI6MTY1ODI3NzY1MSwiZXhwIjoxNjU4MjgxMjUxLCJqdGkiOiJjZWZlMDZhMjUxNDI2ZmFjMGI5Nzk4ZWE4OWRlMDUzN2IwNWFjMmZiIn0.CUSSx2_AARuRhrx87eOSam0ov84wWmHMNoUJ8b2OA4kj2f6xRl5oFxVkxDrAF8R3niWAvo-Ey6VLSNkExAf_WvZSV7bt-V_2u9W4Vy4lrZlGyCSRF-Pcl6i5cCzdmOxQ3hNRvjuLOUT9RGI6NC7r8it8Z6gNVEwHzZCsUTfxJZQvx0-6KwZ01x4_xWWuVvUoktdM3BM6vFH9LepVZ8lH5f5aKX_jtBW98DPma-F5GVPRFo3HS6cMOk9C0eaTNgGQ3mvr0gfIPnntN52ax-4nE3qWoJmR2HQPUQR4Bkv6lLZcEepOUMNyXW9aezJnCsWDJw0-FF4_PCRxwy9m0se_Yw'
    }
    response = requests.request(
        "POST", tour_rec_url, headers=headers, data=payload)
    return json.loads(response.text).get("tour_type")
