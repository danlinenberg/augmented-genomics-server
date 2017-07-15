from __future__ import print_function

import json
import boto3
import csv
import time
import threading
import datetime
import math

def lambda_handler(event, context):

    minutes = 10
    global key
    key = event["Key"]
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('lambda')

    global dct
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

    table_patient = dynamodb.Table("Patient")
    table_doctor = dynamodb.Table("Doctor")

    try:
        response_patient = table_patient.get_item(
            Key={
                'id': int(dct["id"])
            }
        )
        item_patient = response_patient['Item']
    except Exception as e:
        return e


    #super-doctor
    try:
        response_doctor = table_doctor.get_item(
            Key={
                'id': int(dct["doctor"])
            }
        )
        item_doctor = response_doctor['Item']
        if(item_doctor["access"] == 3):
            pl = dict()
            pl['Key'] = str(item_patient['id'])
            queryName = dct['query']
            return get_vcf(client, queryName, json.dumps(pl))
    except Exception as e:
        print(e)
    

    for k,v in dct.items():
        if(k in item_patient):
            if(str(dct[k])!=str(item_patient[k])):
                return "No match on "+k
        elif(k == "timestamp"):
            if(math.ceil(time.time())-int(v)>(60*minutes)):
                return "Expired"
        elif(k == "query"):
            queryName = v
            
    pl = dict()
    pl['Key'] = str(item_patient['id'])    
    
    return get_vcf(client, queryName, json.dumps(pl))


def get_vcf(client, functionName, payload):
    try:
        response = client.invoke(
            FunctionName = "query_handler",
            InvocationType='RequestResponse',
            Payload=json.dumps({"Key": "doctor="+dct['doctor']+"&id="+dct['id']+"&query="+functionName})
        )
        return response['Payload'].read()

    except Exception as e:
        print(e)
        return "No query type found"
