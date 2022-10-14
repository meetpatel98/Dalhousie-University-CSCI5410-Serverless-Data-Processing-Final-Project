import csv

def adminlogin(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    requestData = request.get_json()

    with open('credentials.csv', newline='') as f:
        reader = csv.reader(f)
        credentials = list(reader)

    username = credentials[0][0]
    password = credentials[0][1]
    print(username)
    print(password)
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    if(username == requestData["username"] and password == requestData["password"]):
        res = {
            "message": "Admin Login Successful"
        }
        return (res, 200, headers)

    else:
        res = {
            "message": "Unauthorised User"
        }
        return (res, 401, headers)
