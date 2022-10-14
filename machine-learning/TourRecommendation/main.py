from typing import Dict
import json
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

project ="783409916701"
endpoint_id ="1329643809516027904"
location = "us-central1"
api_endpoint = "us-central1-aiplatform.googleapis.com"

def similarTour(request):
    request_json = request.get_json()
    #capturing number of days from backendAPI
    days_dict={ "days": request_json["days"]}
    
    vertexai_client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": api_endpoint})
    instance = json_format.ParseDict(days_dict, Value())
    
    parameters = json_format.ParseDict({}, Value())
    endpoint = vertexai_client.endpoint_path(project=project, location=location, endpoint=endpoint_id)
    res = vertexai_client.predict(endpoint=endpoint, instances=[instance], parameters=parameters)

    #capturing the predictions
    predictions = res.predictions
    for prediction in predictions:
        val = max(prediction['scores'])
        idx = prediction['scores'].index(val)
        pred = prediction['classes'][idx]
        break
        
    return json.dumps({"tour_type": pred})

