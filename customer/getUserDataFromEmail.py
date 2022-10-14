import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def getUserDataFromEmail(request):
  if request.method == 'OPTIONS':
    headers = {
           'Access-Control-Allow-Origin': '*',
           'Access-Control-Allow-Methods': '*',
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Max-Age': '3600'
      }
    return ('', 204, headers)

  requestData = request.get_json()
  if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    default_app = firebase_admin.initialize_app(cred)

  headers = {
     'Access-Control-Allow-Origin': '*'
  }

  db = firestore.client()
  docs = db.collection('users').stream()
  for doc in docs:
    eachDoc = doc.to_dict()
    if(eachDoc["email"]==requestData["email"]):
      return (eachDoc,200,headers)

  error = {
      "message": "User Not Found"
    }
  return (error,404,headers)
