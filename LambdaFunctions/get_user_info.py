#!/usr/bin/env python3
# Created by Viransh Bhardwaj
# Created on 5th June 2023
#This function returns a row from our project_user DynamoDB


import json
import boto3
import decimal

def replace_decimals(obj):
        # Helper funtion to Decimals in an arbitrary object
        #   from: https://github.com/boto/boto3/issues/369

    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = replace_decimals(v)
        return obj
    elif isinstance(obj, set):
        return set(replace_decimals(i) for i in obj)
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


def lambda_handler(event, context):
    # TODO implement
    
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('project_users')
    try:
        response = table.get_item(
        Key = {
            'email': event['email_address']
            
        })
        
        try:
            result = response['Item']
            result = replace_decimals(result)
        except:
            result = {}
    
        print(result)
    
        return_var ={
            'statusCode': 200,
            'body': json.dumps(result)
        }
    
        return return_var
    except:
        return {
            'statusCode': 204,
            'body': json.dumps({})
        }
    
