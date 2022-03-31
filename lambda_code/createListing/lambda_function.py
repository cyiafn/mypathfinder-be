
import boto3
import json
import re
import datetime
import os

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
            "tokenId": r"^[0-9]{0,9}$",
            "title": r"^[ a-zA-Z0-9]{0,256}$",
            "description": r"^[ a-zA-Z0-9]{0,256}$"
            
        }
        self._requiredAttributes = ["tokenId", "title", "description"]
        self._optionalAttributes = []
        self._listingTableName = os.environ["LISTING_TABLE_NAME"]
    
    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self.validateRequest()
        self.createListing()
        return {"body": "done"}

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
            
    def createListing(self):
        try:
            table = dynamodb.Table(self._listingTableName)

            response = table.get_item(Key={
                    "tokenId": self._validatedRequest["tokenId"]
                })
            if "Item" in response:
                response = table.delete_item(
                    Key={
                        "tokenId": self._validatedRequest["tokenId"]
                    })
            

            log("[ListingDB] Data pulled: " + str(response), "INFO")

            payload = {
                "tokenId": self._validatedRequest["tokenId"],
                "title": self._validatedRequest["title"],
                "description": self._validatedRequest["description"]
                
            }

            response = table.put_item(
                Item=payload
            )
            log("[CreateListing] Successful.", "INFO")
                
        except Exception as e:
            log("[ListingDB] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                    "statusCode": 500,
                    "message": "Error interacting with DB"
                })
            )


def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
    return res


# if __name__ == "__main__":
#     os.environ["LISTING_TABLE_NAME"] = "ProvBE-listing"
#     rrp = RequestResponseProcessor({
#         "tokenId": "1",
#         "title": "Test Title",
#         "description": "Test Description"
#     })
#     rrp.orchestrate()