import boto3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
import uuid

def signup(request):

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

  cred = credentials.Certificate("key.json")
  data = {
    "id": str(uuid.uuid4()),
    "name": requestData["name"],
    "email": requestData["email"],
    "question": requestData["question"],
    "answer": requestData["answer"],
    "key": requestData["key"]
  }
  res = {
    "message": None
  }

  try:
    response = client.sign_up(
    ClientId=poolData["ClientId"],
    Username=requestData["email"],
    Password=requestData["password"],
    UserAttributes=[{"Name": "email", "Value": requestData["email"]}],
    )
    if not firebase_admin._apps:
      cred = credentials.Certificate("key.json")
      default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    eachDoc = db.collection('users').document(str(data["id"]))
    eachDoc.set(data)
    res["message"]="Successfully Signed up. Please verify your email."
  
  except Exception as e:
    print(e.__class__.__name__)
    if(e.__class__.__name__ == "UsernameExistsException"):
      res["message"]= "Email Id already exists."
    else:
      res["message"]="Error : " + e.__class__.__name__
  
  headers = {
     'Access-Control-Allow-Origin': '*'
  }
  
  return (res, 200, headers)