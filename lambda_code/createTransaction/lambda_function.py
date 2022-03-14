'''
This lambda function creates a new transaction record.
@author: Lim Her Huey

@request
requiredAttributes[tokenId, txn_hash, sender, receiver]

@response
errorCode and message on error
statusCode and user data on success
'''

import boto3
import json
import re
import datetime
import os

dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

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
            "tokenId": r"^[0-9]{1,99}$",
            "txn_hash": r"^[0-9a-zA-Z]{1,256}$",
            "sender": r"^[0-9a-zA-Z]{0,99}$",
            "receiver": r"^[0-9a-zA-Z]{0,99}$"
        }
        self._requiredAttributes = ["tokenId", "txn_hash", "sender", "receiver"]
        self._optionalAttributes = []
        self._provbeTransactionTableName = os.environ["PROVBE_TRANSACTION_TABLE_NAME"]
        self._datetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self.validateRequest()
        self.updateDb()
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
        # ensure unvalidated request contains all required attributes
        if not set(self._requiredAttributes).issubset(set(self._unvalidatedRequest.keys())):
            log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
            raise Exception(errorResponse)
        else:
            # ensure unvalidated request does not have extra attributes outside of those specified in required & optional attributes
            if len(set(self._unvalidatedRequest.keys()).intersection(self._requiredAttributes + \
                self._optionalAttributes)) == len(self._unvalidatedRequest.keys()):
                for key, value in self._unvalidatedRequest.items():
                    match = re.findall(self._regex[key], value)
                    # ensure only one match for the regex
                    if len(match) == 1:
                        self._validatedRequest[key] = value
                    else:
                        log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
                        raise Exception(errorResponse)
            else:
                log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
                raise Exception(errorResponse)
        log("[VALIDATION] Success" + str(self._validatedRequest), "INFO")

    def updateDb(self):
        try:
            table = dynamodb.Table(self._provbeTransactionTableName)

            payload = {
                "tokenId": int(self._validatedRequest["tokenId"]),
                "txn_hash": self._validatedRequest["txn_hash"],
                "sender": self._validatedRequest["sender"],
                "receiver": self._validatedRequest["receiver"],
                "datetime": self._datetime
            }

            response = table.put_item(
                Item=payload
            )
            log("[CreateTransactionDB] Successful.", "INFO")
        except Exception as e:
            log("[CreateTransactionDB] Failed.", "ERROR", e)
            raise Exception(json.dumps(
                {
                    "statusCode": 500,
                    "message": "Error interacting with DB"
                })
            )

    def buildResponse(self):
        #code to run incase i need to filter out decimals
        return {
            "statusCode": 200,
            "body": "Updated successfully."
        }


def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
    return res

# if __name__ == "__main__":
#     os.environ["PROVBE_TRANSACTION_TABLE_NAME"] = "provbe-Transaction"
#     e = {
#         "tokenId": "2",
#         "txn_hash": "def",
#         "sender": "0x25f3cc20e429d183657c89535cbef07c3a5f33a3",
#         "receiver": "0xbfa9ddc23732c910c5f1a304c1957f9b979e792f"
#     }
#     lambda_handler(e, {})
