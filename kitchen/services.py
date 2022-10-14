from datetime import datetime
import uuid
from dynamodb import DynamoDB
from dynamo_collections import MEAL, MEAL_ORDER
from handle_notification import post_notification
import json
import requests


def get_meals(logger):
    dynamo = DynamoDB()
    meals = dynamo.get_all_records(MEAL)
    logger.info(meals)
    return None if not meals else meals


def order_meal(logger, meal_id, customer_id, booking_id, quantity, request_id):
    try:
        dynamo = DynamoDB()
        meal = dynamo.get_record(MEAL, {'id': meal_id})
        logger.info(meal)
        total_cost = int(meal[0]['cost']) * int(quantity)
        logger.info(total_cost)
        data = {
            'id': str(uuid.uuid1()),
            'meal_id': meal_id,
            'meal_name': meal[0]['name'],
            'customer_id': customer_id,
            'booking_id': booking_id,
            'quantity': quantity,
            'total_cost': total_cost,
            'timestamp': str(datetime.now())
        }
        dynamo.insert(MEAL_ORDER, data)
        post_notification({
            "customer_id": customer_id,
            "message": "Meal booked for booking {}| Quantity: {} | Total Cost: ${} | Meal Booking date: {}".format(
                booking_id, quantity, total_cost, str(
                    datetime.now().strftime("%B %d, %Y at %H:%M"))
            )
        })
        url = "https://us-central1-sdp-bnb.cloudfunctions.net/pushKitchenMessage"
        payload = json.dumps({
            "request_id": request_id,
            "status": "Complete"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        requests.request("POST", url, headers=headers, data=payload)
        logger.info(f"Meal order status: success | Customer id: {customer_id}")
    except:
        url = "https://us-central1-sdp-bnb.cloudfunctions.net/pushKitchenMessage"
        payload = json.dumps({
            "request_id": request_id,
            "status": "Failed"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        requests.request("POST", url, headers=headers, data=payload)
        logger.info(f"Meal order status: failed | Customer id: {customer_id}")


def get_meal_bookings(logger, customer_id):
    dynamo = DynamoDB()
    bookings = dynamo.get_all_records(MEAL_ORDER)
    customer_meal_booking_details = [
        booking for booking in bookings if booking['customer_id'] == customer_id]
    logger.info(customer_meal_booking_details)
    return customer_meal_booking_details
