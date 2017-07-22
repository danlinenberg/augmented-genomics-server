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
    
    id= int(dct["id"])
    #check if vcf exist
    vcf_exist = client.invoke(
        FunctionName = 'is_vcf_exist',
        InvocationType='RequestResponse',
        Payload=json.dumps({"Key": id})
    )
    if("false" in vcf_exist['Payload'].read()):
        return "No VCF data for this patient"
    
    doctor = dct['doctor']
    is_super_doctor = client.invoke(
        FunctionName = 'access_control_handler',
        InvocationType='RequestResponse',
        Payload=json.dumps({"Key": doctor})
    )
    if(int(is_super_doctor['Payload'].read())==0):
        return get_vcf(client, str(json.dumps(event)))

    table_patient = dynamodb.Table("Patient")
    table_doctor = dynamodb.Table("Doctor")

    try:
        response_patient = table_patient.get_item(
            Key={
                'id': id
            }
        )
        item_patient = response_patient['Item']
    except Exception as e:
        return e

    for k,v in dct.items():
        if(k in item_patient):
            if(str(dct[k])!=str(item_patient[k])):
                return "No match on "+k
        elif(k == "timestamp"):
            if(math.ceil(time.time())-int(v)>(60*minutes)):
                return "Expired"
        elif(k == "query"):
            queryName = v
            
    return get_vcf(client, str(json.dumps(event)))


def get_vcf(client, payload):
    try:
        response = client.invoke(
            FunctionName = 'query_handler',
            InvocationType='RequestResponse',
            Payload=payload
        )
        return response['Payload'].read()[1:-1]
        
    except Exception as e:
        return "Error retrieving data"
