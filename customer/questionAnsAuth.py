import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def questionAnsAuth(request):

  if request.method == 'OPTIONS':
    headers = {
           'Access-Control-Allow-Origin': '*',
           'Access-Control-Allow-Methods': '*',
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Max-Age': '3600'
      }
    return ('', 204, headers)

  securityData = request.get_json()

  response = {
    "id": None,
  }
  error = {
    "message" : None
  }

  if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    default_app = firebase_admin.initialize_app(cred)
    
  db = firestore.client()
  docs = db.collection('users').stream()
  for doc in docs:
    eachDoc = doc.to_dict()
    if(eachDoc["email"]==securityData["email"]):
      response["id"]=doc.id
      print(doc.id)

  print(response)

  headers = {
     'Access-Control-Allow-Origin': '*'
  }

  try:
    doc = db.collection('users').document(response["id"]).get().to_dict()
    securityQuestion = doc["question"]
    securityAnswer = doc["answer"]
  
  except Exception as e:
    error["message"]= e.__class__.__name__
    return (error,400,headers) 

  if(securityQuestion == securityData["question"] and securityAnswer == securityData["answer"]):
    return (response,200,headers)
  
  else:
    error["message"]="Invalid Security Question or Answer"
    return (error,400,headers)