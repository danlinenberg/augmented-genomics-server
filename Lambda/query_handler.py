from __future__ import print_function # Python 2/3 compatibility

import boto3
import json

def lambda_handler(event, context):
    
    key = event["Key"]
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('lambda')

    dct = dict()
    lst = list()
    for p1 in key.split("&"):
        lst=[]
        for p2 in p1.split("="):
            if(p2!=""):
                lst.append(p2)
        try:
            dct[lst[0]]=lst[1]
        except Exception as e:
            pass

    id = dct['id']
    query = dct['query']
    if("clear" in str(query).lower()):
        query="query_naive_all"
    doctor = int(dct['doctor'])
        
    access_response = client.invoke(
        FunctionName='access_control_controller',
        InvocationType='RequestResponse',
        Payload=json.dumps({"Key": id, "doctor": doctor, "request": 1 })
    )
    access = access_response['Payload'].read()    
    
    try:
        response = client.invoke(
            FunctionName=query,
            InvocationType='RequestResponse',
            Payload=json.dumps({"Key": id, "access": access})
        )
        return response['Payload'].read()[1:-1]
    
    except Exception as e:
            return "Failure"
