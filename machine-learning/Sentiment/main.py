from google.cloud import language_v1
import json
import math

nlp_client = language_v1.LanguageServiceClient()

def sentimentAnalysis(request):
  request_json = request.get_json()
  text = request_json["text"]
  
  #get sentiment from natural language
  doc = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
  sentiment = nlp_client.analyze_sentiment(request={"document": doc} ).document_sentiment
  
  if sentiment.score < 0:
    polarity = "NEGATIVE"
  else:
    polarity = "POSITIVE"
  
  #creating sentiment response
  response = {}
  response['feedback'] = text
  score = math.modf((sentiment.score) * 1000)
  response['sentimentscore'] = score[1]
  response['sentimentmagnitude'] = sentiment.magnitude
  response['polarity'] = polarity
  
  return json.dumps(response)
