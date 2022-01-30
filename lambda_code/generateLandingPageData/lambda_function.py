'''
This lambda function returns processed user data to 
the front end to generate personalised data landing page for the user
@author: Benjamin Ho

@request
check postman
RequiredAttribtues : ["Authorization"]
OptionalAttributes : []


@return
errorCode and message on fail
statusCode and body of processed user and GOVApi data on success
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
        # note that event is just the json of tokens passed from FE
        self._unvalidatedRequest = event
        self._validatedRequest = {}
        self._regex = {
            "Authorization": r"^[\w-]*\.[\w-]*\.[\w-]*$"
        }
        self._requiredAttributes = ["Authorization"]
        self._optionalAttributes = []
        self._userTableName = os.environ["USER_TABLE_NAME"]
        self._userData = {}
        self._responseData = {}
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
        self.readDataFromDb()
        self.readFromApi()
        self.evaluateData()
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
            if len(set(self._unvalidatedRequest.keys()).intersection(self._requiredAttributes +
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

    def readDataFromDb(self):
        try:
            table = dynamodb.Table(self._userTableName)
            response = table.get_item(Key={
                "email": self._email
            })
            data = response["Item"]
            self._userData = data

            log("UserDB] Data pulled: " + str(data), "INFO")
        except Exception as e:
            log("[UserDB] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                "statusCode": 500,
                "message": "Error interacting with DB"
            })
            )

    def readFromApi(self):
        '''
        function to call govApi
        '''
        try:
            url = 'https://data.gov.sg/api/action/datastore_search?resource_id=f184a3c8-2d18-4acf-bb50-898aa05e24b7'
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            data = json.loads(r.data.decode('utf-8'))

            log("[GovAPI] Data pulled: " + str(data), "INFO")
        except Exception as e:
            log("[GovAPI] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                "statusCode": 500,
                "message": "Error interacting with GovAPI"
            })
            )

        # initialise dictionary
        for i in range(12, 43, 5):
            self._responseData.update(
                {data["result"]["records"][i]["level_1"]: {}})
        # for 'HDB Dwellings - 1- & 2-Room Flats'
        for i in range(13, 18):
            self._responseData[data["result"]["records"][i]["level_1"]].update(
                {data["result"]["records"][i]["level_2"]: data["result"]["records"][i]["value"]})
        # for 'HDB Dwellings - 3-Room Flats'
        for i in range(19, 24):
            self._responseData[data["result"]["records"][i]["level_1"]].update(
                {data["result"]["records"][i]["level_2"]: data["result"]["records"][i]["value"]})
        # for 'HDB Dwellings - 4-Room Flats'
        for i in range(25, 30):
            self._responseData[data["result"]["records"][i]["level_1"]].update(
                {data["result"]["records"][i]["level_2"]: data["result"]["records"][i]["value"]})
        #  for 'HDB Dwellings - 5-Room & Executive Flats'
        for i in range(31, 36):
            self._responseData[data["result"]["records"][i]["level_1"]].update(
                {data["result"]["records"][i]["level_2"]: data["result"]["records"][i]["value"]})
        # for 'Condominiums & Other Apartments'
        for i in range(37, 42):
            self._responseData[data["result"]["records"][i]["level_1"]].update(
                {data["result"]["records"][i]["level_2"]: data["result"]["records"][i]["value"]})
        # for 'Landed Properties'
        for i in range(43, 48):
            self._responseData[data["result"]["records"][i]["level_1"]].update(
                {data["result"]["records"][i]["level_2"]: data["result"]["records"][i]["value"]})

    def evaluateData(self):
        '''
        evaluate data using api and user data, store proccessed numbers in self._responseData
        '''
        self._responseData.update(
            {"User": {}})
        monthlyIncome = (self._userData["yearly_income"])/12
        # 1 or 2 room hdb
        if self._userData["house_type"] == "HDB" and (self._userData["no_of_room"] == 1 or self._userData["no_of_room"] == 2):
            if monthlyIncome <= int(self._responseData['HDB Dwellings - 1- & 2-Room Flats']['1st - 20th']):
                self._responseData["User"].update(
                    {"Quartile": '1st - 20th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 1- & 2-Room Flats']['21st - 40th']):
                self._responseData["User"].update(
                    {"Quartile": '21st - 40th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 1- & 2-Room Flats']['41st - 60th']):
                self._responseData["User"].update(
                    {"Quartile": '41st - 60th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 1- & 2-Room Flats']['61st - 80th']):
                self._responseData["User"].update(
                    {"Quartile": '61st - 80th'})
            else:
                self._responseData["User"].update(
                    {"Quartile": '81st - 100th'})

        # 3 room hdb
        elif self._userData["house_type"] == "HDB" and self._userData["no_of_room"] == 3:
            if monthlyIncome <= int(self._responseData['HDB Dwellings - 3-Room Flats']['1st - 20th']):
                self._responseData["User"].update(
                    {"Quartile": '1st - 20th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 3-Room Flats']['21st - 40th']):
                self._responseData["User"].update(
                    {"Quartile": '21st - 40th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 3-Room Flats']['41st - 60th']):
                self._responseData["User"].update(
                    {"Quartile": '41st - 60th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 3-Room Flats']['61st - 80th']):
                self._responseData["User"].update(
                    {"Quartile": '61st - 80th'})
            else:
                self._responseData["User"].update(
                    {"Quartile": '81st - 100th'})

        # 4 room hdb
        elif self._userData["house_type"] == 'HDB' and self._userData["no_of_room"] == 4:
            if monthlyIncome <= int(self._responseData['HDB Dwellings - 4-Room Flats']['1st - 20th']):
                self._responseData["User"].update(
                    {"Quartile": '1st - 20th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 4-Room Flats']['21st - 40th']):
                self._responseData["User"].update(
                    {"Quartile": '21st - 40th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 4-Room Flats']['41st - 60th']):
                self._responseData["User"].update(
                    {"Quartile": '41st - 60th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 4-Room Flats']['61st - 80th']):
                self._responseData["User"].update(
                    {"Quartile": '61st - 80th'})
            else:
                self._responseData["User"].update(
                    {"Quartile": '81st - 100th'})

        # 5 room hdb
        elif self._userData["house_type"] == "HDB" and self._userData["no_of_room"] == 5:
            if monthlyIncome <= int(self._responseData['HDB Dwellings - 5-Room & Executive Flats']['1st - 20th']):
                self._responseData["User"].update(
                    {"Quartile": '1st - 20th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 5-Room & Executive Flats']['21st - 40th']):
                self._responseData["User"].update(
                    {"Quartile": '21st - 40th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 5-Room & Executive Flats']['41st - 60th']):
                self._responseData["User"].update(
                    {"Quartile": '41st - 60th'})
            elif monthlyIncome <= int(self._responseData['HDB Dwellings - 5-Room & Executive Flats']['61st - 80th']):
                self._responseData["User"].update(
                    {"Quartile": '61st - 80th'})
            else:
                self._responseData["User"].update(
                    {"Quartile": '81st - 100th'})

        # condo
        elif self._userData["house_type"] == "Condo":
            if monthlyIncome <= int(self._responseData['Condominiums & Other Apartments']['1st - 20th']):
                self._responseData["User"].update(
                    {"Quartile": '1st - 20th'})
            elif monthlyIncome <= int(self._responseData['Condominiums & Other Apartments']['21st - 40th']):
                self._responseData["User"].update(
                    {"Quartile": '21st - 40th'})
            elif monthlyIncome <= int(self._responseData['Condominiums & Other Apartments']['41st - 60th']):
                self._responseData["User"].update(
                    {"Quartile": '41st - 60th'})
            elif monthlyIncome <= int(self._responseData['Condominiums & Other Apartments']['61st - 80th']):
                self._responseData["User"].update(
                    {"Quartile": '61st - 80th'})
            else:
                self._responseData["User"].update(
                    {"Quartile": '81st - 100th'})

        # landed
        elif self._userData["house_type"] == "Landed":
            if monthlyIncome <= int(self._responseData['Landed Properties']['1st - 20th']):
                self._responseData["User"].update(
                    {"Quartile": '1st - 20th'})
            elif monthlyIncome <= int(self._responseData['Landed Properties']['21st - 40th']):
                self._responseData["User"].update(
                    {"Quartile": '21st - 40th'})
            elif monthlyIncome <= int(self._responseData['Landed Properties']['41st - 60th']):
                self._responseData["User"].update(
                    {"Quartile": '41st - 60th'})
            elif monthlyIncome <= int(self._responseData['Landed Properties']['61st - 80th']):
                self._responseData["User"].update(
                    {"Quartile": '61st - 80th'})
            else:
                self._responseData["User"].update(
                    {"Quartile": '81st - 100th'})

        # no house
        else:
            self._responseData["User"].update(
                {"Quartile": 'NIL'})

        self._responseData["User"].update(
            {"Monthly income": str(int(monthlyIncome))})  # update monthly income
        self._responseData["User"].update(
            {"House Type": self._userData["house_type"]})  # update house type
        self._responseData["User"].update(
            {"No of rooms": str(self._userData["no_of_room"])})  # update number of rooms

        self._response = {
            "statusCode": 200,
            "body": self._responseData
        }


def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
