'''
This lambda function gets an array of transactions of a given tokenId.
@author: Lim Her Huey

@request
requiredAttribute[tokenId]

@response
errorCode and message on error
statusCode and user data on success
'''

import boto3
import json
import re
import boto3
import datetime
import os
from boto3.dynamodb.conditions import Key

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
            "tokenId": r"^[0-9]{1,99}$"
        }
        self._requiredAttributes = ["tokenId"]
        self._optionalAttributes = []
        self._provbeTransactionTableName = os.environ["PROVBE_TRANSACTION_TABLE_NAME"]
        self._transactions = []
    
    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self.validateRequest()
        self.getTransactions()
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

    def getTransactions(self):
        '''
        Get array of transactions associated with tokenId from database.
        '''
        try:
            table = dynamodb.Table(self._provbeTransactionTableName)

            response = table.query(
                KeyConditionExpression=Key('tokenId').eq(int(self._validatedRequest["tokenId"]))
            )
            data = response["Items"]
            self._transactions = data

            log("[provbeTransactionDB] Data pulled: " + str(data), "INFO")
        except Exception as e:
            log("[provbeTransactionDB] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                    "statusCode": 404,
                    "message": "Validation failed."
                })
            )
    
    def buildResponse(self):
        #code to run incase i need to filter out decimals
        return {
            "statusCode": 200,
            "body": {
                "transactions": self._transactions
            }
        }


def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
    return res


if __name__ == "__main__":
    os.environ["PROVBE_TRANSACTION_TABLE_NAME"] = "provbe-Transaction"
    e = {
        "tokenId": "54"
    }
    lambda_handler(e, {})