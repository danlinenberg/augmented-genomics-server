from __future__ import print_function

import json
import boto3
import csv
import time
import threading

print('Loading function')

    
def lambda_handler(event, context):
    global key
    key = event["Key"]
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
    
    id = dct["id"]
    level = dct["level"]
    setting = dct["setting"]
    access_header = "access_level_"+str(level)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("Patient")

    try:
        response = table.get_item(
            Key={
                'id': int(id)
            }
        )
    except Exception as e:
        print(e)
        return "No patient found with ID "+str(dct['id'])
    else:
        item = response['Item']
        item[access_header]=setting
        table.put_item(
            Item = item
        )

