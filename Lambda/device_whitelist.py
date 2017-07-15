from __future__ import print_function

import json
import boto3
import csv
import time
import threading

def lambda_handler(event, context):

    global key
    key = event["Key"]
    dynamodb = boto3.resource('dynamodb')

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

    table = dynamodb.Table("Patient")

    try:
        response = table.get_item(
            Key={
                'id': int(dct["id"])
            }
    )
    except Exception as e:
        print(e)
        return "No patient found with ID "+str(dct['id'])
    else:
        item = response['Item']
        for key,value in dct.items():
            if(key!='id' and key!="" and key!=None and value!="" and value!=None):
                item[str(key)]=str(value)
        table.put_item(
            Item = item
        )

        return "Success"
