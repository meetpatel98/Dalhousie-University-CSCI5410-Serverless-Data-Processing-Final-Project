import boto3
import csv

def login(request):

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
    "region":credentialsList[1][0],
    "accessKeyId":credentialsList[1][1],
    "secretAccessKey":credentialsList[1][2]
  }

  poolData = {
    "UserPoolId": credentialsList[1][3],
    "ClientId": credentialsList[1][4],
  }

  client = boto3.client("cognito-idp", 
  region_name=awsCredentials["region"], 
  aws_access_key_id=awsCredentials["accessKeyId"], 
  aws_secret_access_key=awsCredentials["secretAccessKey"])
  headers = {
     'Access-Control-Allow-Origin': '*'
  }

  try:
    response = client.initiate_auth(
    ClientId=poolData["ClientId"],
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={"USERNAME": requestData["email"], "PASSWORD": requestData["password"]},
  )
    access_token = response["AuthenticationResult"]["AccessToken"]
    response = client.get_user(AccessToken=access_token)
    res = {
      "access_token" : access_token,
      "email" : requestData["email"]
    }
    return (res, 200, headers)
  
  except Exception as e:
    if(e.__class__.__name__ == "NotAuthorizedException"):
      err = {
            "error": "Invalid Credentials"
        }
      print(err)
      return (err, 401, headers)

    elif(e.__class__.__name__ == "UserNotConfirmedException"):
      err = {
            "error": "User not verified. Check your email id for verification link"
        }
      print(err)
      return (err, 400, headers)

    else:
      err = {
            "error": e.__class__.__name__
        }
      print(e.__class__.__name__)
      return (err, 400, headers)