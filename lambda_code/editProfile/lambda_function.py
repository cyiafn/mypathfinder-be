'''
This lambda function implements the 
editProfile lambda for users to edit profile in dynamodb
@author: Chen Yifan

@request 
Check postman
RequiredAttributes = ["Authorization"]
OptionalAttributes = ["have_disability_insurance","no_of_room", "oa_saving", "no_of_children", "have_critical_illness_insurance", "have_spouse",\
    "current_debt", "yearly_income", "current_saving", "house_valuation", "have_hospitalisation_insurance", "house_type", "special_saving", "have_life_insurance"]

@response:
errorCode and message
or statusCode and success
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
            "Authorization": r"^[\w-]*\.[\w-]*\.[\w-]*$",
            "no_of_room": r"^[0-9]{1,10}$",
            "oa_saving": r"^[0-9]{1,100}$",
            "no_of_children": r"^[0-9]{1,3}$",
            "have_critical_illness_insurance": r"^true|false$",
            "have_spouse":r"^true|false$",
            "current_debt": r"^[0-9]{1,100}$",
            "yearly_income": r"^[0-9]{1,100}$",
            "current_saving": r"^[0-9]{1,100}$",
            "house_valuation": r"^[0-9]{1,100}$",
            "have_hospitalisation_insurance": r"^true|false$",
            "house_type": r"^[a-zA-Z]{0,6}$",
            "special_saving": r"^[0-9]{1,100}$",
            "have_life_insurance": r"^true|false$",
            "have_disability_insurance": r"^true|false$"
            
        }
        self._requiredAttributes = ["Authorization"]
        self._optionalAttributes = ["have_disability_insurance","no_of_room", "oa_saving", "no_of_children", "have_critical_illness_insurance", "have_spouse",\
            "current_debt", "yearly_income", "current_saving", "house_valuation", "have_hospitalisation_insurance", "house_type", "special_saving", "have_life_insurance"]
        self._userTableName = os.environ["USER_TABLE_NAME"]
        self._email = ""
        self._userDat = {}
    
    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        if len(self._unvalidatedRequest) == 1:
            raise Exception(json.dumps({
                "statusCode": 400,
                "message": "Nothing to update!"
            }))
        self.validateRequest()
        self.getEmail()
        self.getProfile()
        self.reprocessAnswers()
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
        if not set(self._requiredAttributes).issubset(set(self._unvalidatedRequest.keys())) or len(self._requiredAttributes) > len(self._unvalidatedRequest.keys()):
            log("[VALIDATION] Failed due to required Attributes not present.", "INFO")
            raise Exception(errorResponse)
        else:
            if len(set(self._unvalidatedRequest.keys()).intersection(self._requiredAttributes + \
                self._optionalAttributes)) == len(self._unvalidatedRequest.keys()):
                for key, value in self._unvalidatedRequest.items():
                    match = re.findall(self._regex[key], str(value))
                    if len(match) == 1:
                        self._validatedRequest[key] = value
                    else:
                        log("[VALIDATION] Failed due to required Attributes not present." + key, "INFO")
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

    def reprocessAnswers(self):
        del self._validatedRequest["Authorization"]
        del self._userDat["recommendation_id"]
        for key, value in self._validatedRequest.items():
            self._userDat[key] = value

        self._userDat["yearly_income"] = float(self._userDat["yearly_income"])
        self._userDat["current_saving"] = float(self._userDat["current_saving"])
        self._userDat["current_debt"] = float(self._userDat["current_debt"])
        self._userDat["oa_saving"] = float(self._userDat["oa_saving"])
        self._userDat["special_saving"] = float(self._userDat["special_saving"])
        self._userDat["no_of_children"] = int(self._userDat["no_of_children"])
        self._userDat["house_valuation"] = float(self._userDat["house_valuation"])
        self._userDat["no_of_room"] = int(self._userDat["no_of_room"])
        print("==========\n\n", self._userDat)
        try:
            response = lambda_client.invoke(FunctionName='processAnswers', 
                                InvocationType='RequestResponse',
                                Payload=json.dumps(self._userDat))
            self._userDat["recommendation_id"] = json.loads(json.loads(response.get('Payload').read()))["recommendation_id"]
            log("[processAnswers] Call Success.", "INFO")
            
            
        except Exception as e:
            log("[processAnswers] Call Failed.", "ERROR", e)
            raise Exception(json.dumps(
                {
                    "statusCode": 500,
                    "message": "Unable to process answers"
                })
            )

    def updateDb(self):

        '''
        Update db with new user details

        
        '''

        self._userDat["yearly_income"] = Decimal(self._userDat["yearly_income"])
        self._userDat["current_saving"] = Decimal(self._userDat["current_saving"])
        self._userDat["current_debt"] = Decimal(self._userDat["current_debt"])
        self._userDat["oa_saving"] = Decimal(self._userDat["oa_saving"])
        self._userDat["special_saving"] = Decimal(self._userDat["special_saving"])
        self._userDat["no_of_children"] = Decimal(self._userDat["no_of_children"])
        self._userDat["house_valuation"] = Decimal(self._userDat["house_valuation"])
        self._userDat["no_of_room"] = Decimal(self._userDat["no_of_room"])
        self._userDat["recommendation_id"] = Decimal(self._userDat["recommendation_id"])

        try:
            table = dynamodb.Table(self._userTableName)
            response = table.update_item(
                Key={
                    "email": self._email
                },
                UpdateExpression="set have_disability_insurance=:a, oa_saving=:b, no_of_room=:c, no_of_children=:d, have_critical_illness_insurance=:e, have_spouse=:f, current_debt=:g, yearly_income=:h, current_saving=:i, house_valuation=:j, have_hospitalisation_insurance=:k, house_type=:l, special_saving=:m, have_life_insurance=:n, recommendation_id=:o",
                ExpressionAttributeValues={
                    ':a': self._userDat["have_disability_insurance"],
                    ':b': self._userDat["oa_saving"],
                    ':c': self._userDat["no_of_room"],
                    ':d': self._userDat["no_of_children"],
                    ':e': self._userDat["have_critical_illness_insurance"],
                    ':f': self._userDat["have_spouse"],
                    ':g': self._userDat["current_debt"],
                    ':h': self._userDat["yearly_income"],
                    ':i': self._userDat["current_saving"],
                    ':j': self._userDat["house_valuation"],
                    ':k': self._userDat["have_hospitalisation_insurance"],
                    ':l': self._userDat["house_type"],
                    ':m': self._userDat["special_saving"],
                    ':n': self._userDat["have_life_insurance"],
                    ':o': self._userDat["recommendation_id"]
                },
                ReturnValues="UPDATED_NEW"
            )

            log("UserDB] Data updated: " + str(response), "INFO")
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
            "body": "Updated successfully."
        }





def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
    return res