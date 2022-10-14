import random
import decimal
import sys
import subprocess
import json

subprocess.call('pip install requests -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')

import requests


def random_num():
    return decimal.Decimal(random.randrange(1000, 50000)) / 100


def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']


def get_slot(intent_request, slot_name):
    slots = get_slots(intent_request)
    if slots is not None and slot_name in slots and slots[slot_name] is not None:
        return slots[slot_name]['value']['interpretedValue']
    else:
        return None


def get_session_attributes(intent_request):
    session_state = intent_request['sessionState']
    if 'sessionAttributes' in session_state:
        return session_state['sessionAttributes']

    return {}


def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [message],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def elicit_slot(intent_request, session_attributes, slot_to_elicit, message):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit,
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message
        }],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message
        }],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def book_hotel(intent_request):
    session_attributes = get_session_attributes(intent_request)

    complete = get_slot(intent_request, 'Complete')
    room_id = get_slot(intent_request, 'RoomId')
    from_date = get_slot(intent_request, 'FromDate')
    to_date = get_slot(intent_request, 'ToDate')
    confirm_email = get_slot(intent_request, 'ConfirmEmail')

    if not from_date:
        return elicit_slot(intent_request, session_attributes, 'FromDate',
                           "What's the check-in date?")
    if not to_date:
        return elicit_slot(intent_request, session_attributes, 'ToDate',
                           "What's the check-out date?")

    if from_date and to_date and not room_id:
        rooms = get_available_rooms(from_date, to_date)
        return elicit_slot(intent_request, session_attributes, 'RoomId',
                           "Choose one of the following, reply with the number: {}"
                           .format(print_rooms(rooms)))

    if not complete:
        return elicit_slot(intent_request, session_attributes, 'Complete',
                           'You have requested for room option ({}), from {} to {}, say "yes" to continue and "no" to cancel'
                           .format(int(room_id), from_date, to_date))

    if not confirm_email:
        return elicit_slot(intent_request, session_attributes, 'ConfirmEmail',
                           'Enter registered email address to place the order')

    if complete.lower() == "yes":
        customer = get_customer(confirm_email)
        if customer.get("id"):
            rooms = get_available_rooms(from_date, to_date)
            book_room(rooms[int(room_id)]["id"], customer["id"], from_date, to_date)
            return close(intent_request, session_attributes, "Fulfilled", "Your request has been placed successfully")
        else:
            return close(intent_request, session_attributes, "Fulfilled", "User not registered!")
    elif complete.lower() == "no":
        return close(intent_request, session_attributes, "Fulfilled", "Alright! I have cancelled the booking")
    else:
        return elicit_slot(intent_request, session_attributes, 'Complete',
                           'Choose a valid option (yes or no)?')


def order_food(intent_request):
    session_attributes = get_session_attributes(intent_request)

    complete = get_slot(intent_request, 'Complete')
    meal_id = get_slot(intent_request, 'MealId')
    quantity = get_slot(intent_request, 'Quantity')
    confirm_email = get_slot(intent_request, 'ConfirmEmail')

    if not meal_id:
        meals = get_available_meals()
        return elicit_slot(intent_request, session_attributes, 'MealId',
                           "Choose one of the following, reply with the number: {}"
                           .format(print_meals(meals)))

    if not quantity:
        return elicit_slot(intent_request, session_attributes, 'Quantity',
                           "How many of those (Quantity)?")

    if not complete:
        return elicit_slot(intent_request, session_attributes, 'Complete',
                           'You have requested for {} of meal option ({}), say "yes" to continue and "no" to cancel'
                           .format(quantity, int(meal_id)))

    if not confirm_email:
        return elicit_slot(intent_request, session_attributes, 'ConfirmEmail',
                           'Enter registered email address to place the order')

    if confirm_email and complete.lower() == "yes":
        customer = get_customer(confirm_email)
        if customer.get("id"):
            meals = get_available_meals()
            order_meals(meals[int(meal_id)]["id"], customer["id"], quantity)
            return close(intent_request, session_attributes, "Fulfilled", "Your order has been placed successfully")
        else:
            return close(intent_request, session_attributes, "Fulfilled", "User not registered!")
    elif complete.lower() == "no":
        return close(intent_request, session_attributes, "Fulfilled", "Alright! I have cancelled the order")
    else:
        return elicit_slot(intent_request, session_attributes, 'Complete',
                           'Choose a valid option (yes or no)?')


def book_tour(intent_request):
    session_attributes = get_session_attributes(intent_request)

    complete = get_slot(intent_request, 'Complete')
    tour_id = get_slot(intent_request, 'TourId')
    days = get_slot(intent_request, 'NumberOfDays')
    quantity = get_slot(intent_request, 'Quantity')
    confirm_email = get_slot(intent_request, 'ConfirmEmail')

    if not days:
        return elicit_slot(intent_request, session_attributes, 'NumberOfDays',
                           "For how many of days?")

    if not tour_id:
        tours = get_available_tours(days)
        return elicit_slot(intent_request, session_attributes, 'TourId',
                           "Choose one of the following, reply with the number: {}"
                           .format(print_tours(tours)))

    if not quantity:
        return elicit_slot(intent_request, session_attributes, 'Quantity',
                           "How many tickets?")

    if not complete:
        return elicit_slot(intent_request, session_attributes, 'Complete',
                           'You have requested for {} option ({}) tour(s), say "yes" to continue and "no" to cancel'
                           .format(int(quantity), int(tour_id)))

    if not confirm_email:
        return elicit_slot(intent_request, session_attributes, 'ConfirmEmail',
                           'Enter registered email address to place the order')

    if confirm_email and complete.lower() == "yes":
        customer = get_customer(confirm_email)
        if customer.get("id"):
            tours = get_available_tours(days)
            book_tours(tours[int(tour_id)]["id"], customer["id"], quantity)
            return close(intent_request, session_attributes, "Fulfilled", "Your order has been placed successfully")
        else:
            return close(intent_request, session_attributes, "Fulfilled", "User not registered!")
    elif complete.lower() == "no":
        return close(intent_request, session_attributes, "Fulfilled", "Alright! I have cancelled the order")
    else:
        return elicit_slot(intent_request, session_attributes, 'Complete',
                           'Choose a valid option (yes or no)?')


def navigate(intent_request):
    session_attributes = get_session_attributes(intent_request)
    page = get_slot(intent_request, 'Page')

    if not page:
        return elicit_slot(intent_request, session_attributes, 'Page',
                           "Which page? Choose one: Login, Register, Room booking, Food orders, Tour booking")

    if page.lower() == "login":
        return close(intent_request, session_attributes, "Fulfilled", "Head to /login")

    if page.lower() == "register":
        return close(intent_request, session_attributes, "Fulfilled", "Head to /register")

    if page.lower() == "room booking":
        return close(intent_request, session_attributes, "Fulfilled", "Head to /rooms")

    if page.lower() == "food orders":
        return close(intent_request, session_attributes, "Fulfilled", "Head to /food")

    if page.lower() == "tour booking":
        return close(intent_request, session_attributes, "Fulfilled", "Head to /tours")


def get_customer(email):
    url = "https://us-central1-serverless-a4-355004.cloudfunctions.net/getUserDataFromEmail"
    payload = json.dumps({
        "email": email
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response


def get_available_rooms(from_date, to_date):
    url = "https://vgjfo3gxbacdua7gokt7qfkjle0xobth.lambda-url.us-east-1.on.aws/get_available_rooms"
    payload = json.dumps({
        "checkin_date": from_date.replace("-", "/"),
        "checkout_date": to_date.replace("-", "/")
    })
    print(from_date, to_date)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response


def get_available_meals():
    url = "https://bvbszg7e4zei52hlynjvpmqnzi0cldfx.lambda-url.us-east-1.on.aws/get_meals"
    response = requests.request("GET", url, headers={}, data="").json()
    print(response)
    return response


def get_available_tours(days):
    url = "https://fjowpswk6sbpmhewgh4mim3ye40ownzj.lambda-url.us-east-1.on.aws/get_tours"
    payload = json.dumps({
        "num_of_days": int(days)
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response


def book_room(room_id, customer_id, from_date, to_date):
    url = "https://vgjfo3gxbacdua7gokt7qfkjle0xobth.lambda-url.us-east-1.on.aws/book_room"

    payload = json.dumps({
        "room_id": room_id,
        "customer_id": customer_id,
        "checkin_date": from_date.replace("-", "/"),
        "checkout_date": to_date.replace("-", "/")
    })
    print(room_id, customer_id, from_date, to_date)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)


def order_meals(meal_id, customer_id, quantity):
    url = "https://bvbszg7e4zei52hlynjvpmqnzi0cldfx.lambda-url.us-east-1.on.aws/order_meal"

    payload = json.dumps({
        "meal_id": meal_id,
        "customer_id": customer_id,
        "quantity": int(quantity)
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)


def book_tours(tour_id, customer_id, quantity):
    url = "https://fjowpswk6sbpmhewgh4mim3ye40ownzj.lambda-url.us-east-1.on.aws/book_tour"

    payload = json.dumps({
        "tour_id": tour_id,
        "customer_id": customer_id,
        "quantity": int(quantity)
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)


def print_rooms(rooms):
    output = ""
    for i in range(len(rooms)):
        output += 'Option {}: {} {} bed(s) for ${} per day. '.format(i, rooms[i].get("no_of_beds"),
                                                                     rooms[i].get("bed_type"),
                                                                     rooms[i].get("cost_per_day"))

    return output


def print_meals(meals):
    output = ""
    for i in range(len(meals)):
        output += 'Option {}: {} for ${}. '.format(i, meals[i].get("name"),
                                                   meals[i].get("cost"))

    return output


def print_tours(tours):
    output = ""
    for i in range(len(tours)):
        output += 'Option {}: {} for ${}. '.format(i, tours[i].get("tour_name"),
                                                   tours[i].get("cost"))

    return output


def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']

    if intent_name == 'BookHotel':
        return book_hotel(intent_request)
    if intent_name == 'OrderFood':
        return order_food(intent_request)
    if intent_name == 'BookTour':
        return book_tour(intent_request)
    if intent_name == 'Navigation':
        return navigate(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    response = dispatch(event)
    return response

