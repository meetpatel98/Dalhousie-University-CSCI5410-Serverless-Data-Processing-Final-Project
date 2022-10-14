import boto3
import uuid
import csv


def userLogs(request):

    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    requestData = request.get_json()

    with open('key.csv', newline='') as f:
        reader = csv.reader(f)
        credentialsList = list(reader)

    awsCredentials = {
        "region": credentialsList[1][0],
        "accessKeyId": credentialsList[1][1],
        "secretAccessKey": credentialsList[1][2]
    }
    TableName = "logs"

    dynamo = boto3.resource('dynamodb',
                            region_name=awsCredentials["region"],
                            aws_access_key_id=awsCredentials["accessKeyId"],
                            aws_secret_access_key=awsCredentials["secretAccessKey"])
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    data = {
        "logId": str(uuid.uuid4()),
        "customerId": requestData["customerId"],
        "email": requestData["email"],
        "loginTimestamp": requestData["loginTimestamp"],
        "logoutTimestamp": requestData["logoutTimestamp"],
    }
    try:
        table = dynamo.Table(TableName)
        response = table.put_item(
            Item=data
        )
        res = {
            "message": "log updated"
        }
        return (res, 200, headers)

    except Exception as e:
        err = {
            "error": "Server Error " + e.__class__.__name__
        }
        return (err, 400, headers)
