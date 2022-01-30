'''
This lambda function return the user profile to frontend
@author: Chen Yifan

@request
requiredAttribute[Authorization]

@response
errorCode and message on error
statusCode and user data on success
'''

import boto3
import json
import re
import boto3 
import time
import datetime
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

#logging func
def log(msg, level, trace = "NULL"):
    if trace == "NULL":
        print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ " " + "[" + level + "]" + " " + msg)
    else:
        print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ " " + "[" + level + "]" + " " + msg, trace)

class RequestResponseProcessor:
    '''
    Class handler for request
    '''
    def __init__(self, event):
        self._unvalidatedRequest = event
        self._validatedRequest = {}
        self._regex = {
            "Authorization": r"^[\w-]*\.[\w-]*\.[\w-]*$"
        }
        self._requiredAttributes = ["Authorization"]
        self._optionalAttributes = []
        self._userTableName = os.environ["USER_TABLE_NAME"]
        self._email = ""
        self._userDat = {}
    
    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self.validateRequest()
        self.getEmail()
        self.getProfile()
        return self.buildResponse()

    def validateRequest(self):
        '''
        Code for validating requests
        '''
        #Predefining errorResponse
        errorResponse = json.dumps({
            "statusCode": 400,
            "message": "Validation failed."
        })
        if not set(self._requiredAttributes).issubset(set(self._unvalidatedRequest.keys())) or len(self._requiredAttributes) > len(self._unvalidatedRequest.keys()):
            log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
            raise Exception(errorResponse)
        else:
            if len(set(self._unvalidatedRequest.keys()).intersection(self._requiredAttributes + \
                self._optionalAttributes)) == len(self._unvalidatedRequest.keys()):
                for key, value in self._unvalidatedRequest.items():
                    match = re.findall(self._regex[key], value)
                    if len(match) == 1:
                        self._validatedRequest[key] = value
                    else:
                        log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
                        raise Exception(errorResponse)
            else:
                log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
                raise Exception(errorResponse)
        log("[VALIDATION] Success" + str(self._validatedRequest), "INFO")

    def getEmail(self):
        '''
        Gets user based on access_token and gets email
        '''
        try:
            cognitoClient = boto3.client('cognito-idp')
            response = cognitoClient.get_user(
                AccessToken=self._validatedRequest["Authorization"]
            )
            for i in response['UserAttributes'][::-1]:
                if i["Name"] == "email":
                    self._email = i["Value"]
                    break

            log("[Cognito] Pulled data for user success: " + str(self._email), "INFO")
        except Exception as e:
            log("[Cognito] Accessing cognito using access_token failed.", "ERROR", e)
            raise Exception(json.dumps({
                "statusCode": 500,
                "message": "Accessing cognito failed."
            }))

    def getProfile(self):
        '''
        reading from db
        '''
        try:
            table = dynamodb.Table(self._userTableName)

            response = table.get_item(Key={
                    "email": self._email
                })
            data = response["Item"]
            self._userDat = data

            log("UserDB] Data pulled: " + str(data), "INFO")
        except Exception as e:
            log("[UserDB] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                    "statusCode": 500,
                    "message": "Error interacting with DB"
                })
            )
    
    def buildResponse(self):
        #code to run incase i need to filter out decimals
        return {
            "statusCode": 200,
            "body": self._userDat
        }



def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
    return res
