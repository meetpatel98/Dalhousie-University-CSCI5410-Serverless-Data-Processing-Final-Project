import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def caesarCipherAuth(request):

  if request.method == 'OPTIONS':
    headers = {
           'Access-Control-Allow-Origin': '*',
           'Access-Control-Allow-Methods': '*',
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Max-Age': '3600'
      }
    return ('', 204, headers)

  cipherData = request.get_json()
  
  if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    default_app = firebase_admin.initialize_app(cred)

  db = firestore.client()
  doc_ref = db.collection('users').document(cipherData["customerId"])
  doc = doc_ref.get()
  doc = doc.to_dict()

  result = ""
  response={
        "state": False
      }
  for i in range(len(cipherData["text"])):
    letter = cipherData["text"][i]
    result+=chr((ord(letter)+doc["key"] -97) % 26 +97)
    if(result == cipherData["decoded"]):
      response["state"]= True

  headers = {
     'Access-Control-Allow-Origin': '*'
  }
  return (response,200,headers)
