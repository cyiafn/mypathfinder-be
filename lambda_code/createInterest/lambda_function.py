'''
This lambda function creates an entry in the database 
table "HousingInterest' or "InsuranceInterest" depending on the type of interest
@author: Benjamin Ho

@request
check postman
RequiredAttributes = ["Authorization", "type", "id"]
OptionalAttributes = []

@return
errorCode and message on fail
statusCode and body of success message on success
'''

import boto3
import json
import re
import boto3
import time
import datetime
import os
import urllib3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


def log(msg, level, trace="NULL"):
    if trace == "NULL":
        print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
              " " + "[" + level + "]" + " " + msg)
    else:
        print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
              " " + "[" + level + "]" + " " + msg, trace)


class RequestResponseProcessor:
    '''
    Class handler for request
    '''

    def __init__(self, event):
        self._email = ""
        self._unvalidatedRequest = event
        self._validatedRequest = {}
        self._regex = {
            "Authorization": r"^[\w-]*\.[\w-]*\.[\w-]*$",
            "idHousing": r"^[h][\w-]*",
            "idInsurance": r"^[i][\w-]*"
        }
        self._requiredAttributes = ["Authorization", "type", "id"]
        self._optionalAttributes = []
        self._housingInterestTableName = os.environ["HOUSING_INTEREST_TABLE_NAME"]
        self._insuranceInterestTableName = os.environ["INSURANCE_INTEREST_TABLE_NAME"]
        self._response = {
            "statusCode": 200,
            "body": ""
        }

    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self.validateRequest()
        self.readEmailFromCognito()
        self.writeToDb()
        return self._response

    def validateRequest(self):
        errorResponse = json.dumps({
            "statusCode": 400,
            "message": "Validation failed."
        })

        if not set(self._requiredAttributes).issubset(set(self._unvalidatedRequest.keys())) or len(self._requiredAttributes) > len(self._unvalidatedRequest.keys()):
            log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
            raise Exception(errorResponse)
        else:
            if len(set(self._unvalidatedRequest.keys()).intersection(self._requiredAttributes + self._optionalAttributes)) == len(self._unvalidatedRequest.keys()):
                match = re.findall(
                    self._regex["Authorization"], self._unvalidatedRequest["Authorization"])
                if len(match) == 1:
                    self._validatedRequest["Authorization"] = self._unvalidatedRequest["Authorization"]
                else:
                    log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
                    raise Exception(errorResponse)

                if self._unvalidatedRequest["type"] == "house":
                    match = re.findall(
                        self._regex["idHousing"], self._unvalidatedRequest["id"])
                    if len(match) == 1:
                        self._validatedRequest["id"] = self._unvalidatedRequest["id"]
                    else:
                        log("[VALIDATION] Failed due to wrong Attributes.", "INFO")
                        raise Exception(errorResponse)
                elif self._unvalidatedRequest["type"] == "insurance":
                    match = re.findall(
                        self._regex["idInsurance"], self._unvalidatedRequest["id"])
                    if len(match) == 1:
                        self._validatedRequest["id"] = self._unvalidatedRequest["id"]
                    else:
                        log("[VALIDATION] Failed due to wrong Attributes.", "INFO")
                        raise Exception(errorResponse)

                if (self._unvalidatedRequest["type"] != "house") and (self._unvalidatedRequest["type"] != "insurance"):
                    log("[VALIDATION] Failed due to wrong Attributes.", "INFO")
                    raise Exception(errorResponse)
                else:
                    self._validatedRequest["type"] = self._unvalidatedRequest["type"]
            else:
                log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
                raise Exception(errorResponse)

        log("[VALIDATION] Success" + str(self._validatedRequest), "INFO")

    def readEmailFromCognito(self):
        # use accessToken to get user email
        try:
            cognitoClient = boto3.client('cognito-idp')
            response = cognitoClient.get_user(
                AccessToken=self._validatedRequest["Authorization"]
            )
            for i in response['UserAttributes'][::-1]:
                if i["Name"] == "email":
                    self._email = i["Value"]
                    break

            log("[Cognito] Pulled data for user success: " +
                str(self._email), "INFO")
        except Exception as e:
            log("[Cognito] Accessing cognito using access_token failed.", "ERROR", e)
            raise Exception(json.dumps({
                "statusCode": 500,
                "message": "Accessing cognito failed."
            }))

    def writeToDb(self):

        if self._validatedRequest["type"] == "house":
            try:
                table = dynamodb.Table(self._housingInterestTableName)

                response = table.put_item(
                    Item={
                        "user_email": str(self._email),
                        "has_handled": "false",
                        "house_id": self._validatedRequest["id"]
                    }
                )
            except Exception as e:
                log("[HousingInterestDB] Failed.", "ERROR", e)
                raise Exception(json.dumps(
                    {
                        "statusCode": 500,
                        "message": "Error interacting with DB"
                    })
                )
        else:
            try:
                table = dynamodb.Table(self._insuranceInterestTableName)

                response = table.put_item(
                    Item={
                        "user_email": str(self._email),
                        "has_handled": "false",
                        "plan_id": self._validatedRequest["id"]
                    }
                )
            except Exception as e:
                log("[InsuranceInterestDB] Failed.", "ERROR", e)
                raise Exception(json.dumps(
                    {
                        "statusCode": 500,
                        "message": "Error interacting with DB"
                    })
                )

        self._response = {
            "statusCode": 200,
            "body": "success"
        }


def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
    return res
