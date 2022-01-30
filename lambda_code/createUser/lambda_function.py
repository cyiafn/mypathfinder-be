'''
This lambda function implements the 
createUser post confirmation lambda trigger for user creation
@author: Chen Yifan

@request body
{
    postConfirmation congito request
}
@response @request callback

'''


import boto3
import json
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
    def __init__(self, event, email):
        self._user = User(event, email)
        self.userTableName = os.environ["USER_TABLE_NAME"]
    
    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self._user.generateRecommendationId()
        self._user.createUser(self.userTableName)

            
class User:
    def __init__(self, event, email):
        self._email = email
        self._yearly_income = float(event["yearly_income"])
        self._current_saving = float(event["current_saving"])
        self._current_debt =float(event["current_debt"])
        self._have_spouse = event["have_spouse"]
        self._oa_saving = float(event["oa_saving"])
        self._special_saving = float(event["special_saving"])
        self._no_of_children = int(event["no_of_children"])
        self._house_type = event["house_type"]
        self._house_valuation = float(event["house_valuation"])
        self._no_of_room = int(event["no_of_room"])
        self._have_life_insurance = event["have_life_insurance"]
        self._have_disability_insurance = event["have_disability_insurance"]
        self._have_hospitalisation_insurance = event["have_hospitalisation_insurance"]
        self._have_critical_illness_insurance = event["have_critical_illness_insurance"]
        self._recommendation_id = None

    def generatePayload(self):
        return {
            "yearly_income": self._yearly_income,
            "current_saving": self._current_saving,
            "current_debt": self._current_debt,
            "have_spouse": self._have_spouse,
            "oa_saving": self._oa_saving,
            "special_saving": self._oa_saving,
            "no_of_children": self._no_of_children,
            "house_type": self._house_type,
            "house_valuation": self._house_valuation,
            "no_of_room": self._no_of_room,
            "have_life_insurance": self._have_life_insurance,
            "have_disability_insurance": self._have_disability_insurance,
            "have_hospitalisation_insurance": self._have_hospitalisation_insurance,
            "have_critical_illness_insurance": self._have_critical_illness_insurance
        }
    
    def generatePayloadDec(self):
        return {
            "yearly_income": Decimal(self._yearly_income),
            "current_saving": Decimal(self._current_saving),
            "current_debt": Decimal(self._current_debt),
            "have_spouse": self._have_spouse,
            "oa_saving": Decimal(self._oa_saving),
            "special_saving": Decimal(self._oa_saving),
            "no_of_children": self._no_of_children,
            "house_type": self._house_type,
            "house_valuation": Decimal(self._house_valuation),
            "no_of_room": self._no_of_room,
            "have_life_insurance": self._have_life_insurance,
            "have_disability_insurance": self._have_disability_insurance,
            "have_hospitalisation_insurance": self._have_hospitalisation_insurance,
            "have_critical_illness_insurance": self._have_critical_illness_insurance
        }
    
    def generateRecommendationId(self):
        try:
            response = lambda_client.invoke(FunctionName='processAnswers', 
                                InvocationType='RequestResponse',
                                Payload=json.dumps(self.generatePayload()))
            self._recommendation_id = json.loads(json.loads(response.get('Payload').read()))["recommendation_id"]
            log("[processAnswers] Call Success.", "INFO")
            
            
        except Exception as e:
            log("[processAnswers] Call Failed.", "ERROR", e)
            raise Exception(json.dumps(
                {
                    "statusCode": 500,
                    "message": "Unable to process answers"
                })
            )

    def createUser(self, userTableName):
        try:
            table = dynamodb.Table(userTableName)

            payload = self.generatePayloadDec()
            payload["email"] = self._email
            payload["recommendation_id"] = self._recommendation_id
            payload["created_at"]: str(int(time.time()))

            response = table.put_item(
                Item=payload
            )
            log("[CreateUser] Successful.", "INFO")
        except Exception as e:
            log("[CreateUserDB] Failed.", "ERROR", e)
            raise Exception(json.dumps(
                {
                    "statusCode": 500,
                    "message": "Error interacting with DB"
                })
            )
    
        

def lambda_handler(event, context):
    log("[REQUEST] " + str(event), "INFO")
    if event["triggerSource"] != "PostConfirmation_ConfirmSignUp":
        log("[REQUEST] filter for confirm password. " + str(event), "INFO")
        return event
    req = RequestResponseProcessor(event["request"]["clientMetadata"], event["request"]["userAttributes"]["email"])
    req.orchestrate()
    return event
