'''
This lambda function implements the pagination and
listing generation function.
@author: Chen Yifan

@request
check postman
requiredAttributes = ["Authorization", "page"]
optionalAttributes = ["min_amount", "max_amount", "min_bedroom", "max_bedroom",
        "min_bathroom", "max_bathroom", "min_sqfeet", "max_sqfeet", "type"]

@response
errorCode and message on fail
statusCode and body of house arrays on success
'''

import boto3
import json
import re
import boto3 
import time
import datetime
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

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
            "page": r"^[0-9]{1,100}$",
            "Authorization": r"^[\w-]*\.[\w-]*\.[\w-]*$",
            "min_amount": r"^[0-9]{1,10}$",
            "max_amount": r"^[0-9]{5,10}$",
            "min_bedroom": r"^[0-9]{1,2}$",
            "max_bedroom": r"^[0-9]{1,2}$",
            "min_bathroom": r"^[0-9]{1,2}$",
            "max_bathroom": r"^[0-9]{1,2}$",
            "min_sqfeet": r"^[0-9]{2,10}$",
            "max_sqfeet": r"^[0-9]{2,10}$",
            "type": r"^(HDB|Landed|Condo|All)$"
        }
        self._paginationSize = int(os.environ["PAGINATION_SIZE"])
        self._userTableName = os.environ["USER_TABLE_NAME"]
        self._houseTableName = os.environ["HOUSING_TABLE_NAME"]
        self._companyTableName = os.environ["COMPANY_TABLE_NAME"]
        self._requiredAttributes = ["Authorization", "page"]
        self._optionalAttributes = ["min_amount", "max_amount", "min_bedroom", "max_bedroom",
        "min_bathroom", "max_bathroom", "min_sqfeet", "max_sqfeet", "type"]
        self._email = ""
        self._userRecommendationId = ""
        self._dat = []
    
    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self.validateRequest()
        if "Authorization" in self._validatedRequest and "page" in self._validatedRequest\
             and len(self._validatedRequest) == 2:
            self.getEmail()
            self.getRecommendationId()
            self.getRecommendationBasedOnId()
            self.getCompany()
        else:
            self.getRecommendationBasedOnFilter()
            self.getCompany()


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
                    if key not in self._regex:
                        self._validatedRequest[key] = value
                        continue
                    match = re.findall(self._regex[key], str(value))
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

    def getRecommendationId(self):
        '''
        Get recommendation ID for user.
        '''
        try:
            table = dynamodb.Table(self._userTableName)

            response = table.get_item(Key={
                    "email": self._email
                })
            data = response["Item"]
            self._userRecommendationId = str(data["recommendation_id"])

            log("UserDB] Data pulled: " + str(data), "INFO")
        except Exception as e:
            log("[UserDB] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                    "statusCode": 500,
                    "message": "Error interacting with DB"
                })
            )

    def getHouseDataRecId(self, timesToPagination):
        try:
            table = dynamodb.Table(self._houseTableName)

            response = table.query(
                IndexName="house_recommendation_id-index",
                KeyConditionExpression=Key('house_recommendation_id').eq(self._userRecommendationId),
            )
            data = response["Items"]
            for i in range(timesToPagination):
                response = table.query(
                    IndexName="house_recommendation_id-index",
                    KeyConditionExpression=Key('house_recommendation_id').eq(self._userRecommendationId),
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                data = response['Items']
            log("houseDB] Data pulled: " + str(data), "INFO")
            return data
            
        except Exception as e:
                log("[houseDB] Failed.", "ERROR", e)
                raise Exception(json.dumps({
                        "statusCode": 500,
                        "message": "Error interacting with DB"
                    })
                )


    def getRecommendationBasedOnId(self):
        eachPagination = 100/self._paginationSize
        page = int(self._validatedRequest["page"])
        if page > eachPagination:
            #1 page = self._pagination size
            timesToPagination = 0
            while page > eachPagination:
                page -= eachPagination
                timesToPagination += 1
            
            data = self.getHouseDataRecId(timesToPagination)
            self._dat = self.retrievePageFromArray(data, page)
        else:
            data = self.getHouseDataRecId(0)
            self._dat = self.retrievePageFromArray(data,page)


    def getHouseDataFilter(self):
        try:
            table = dynamodb.Table(self._houseTableName)

            response = table.scan()
            data = response['Items']
            #this is internal pagination, scan can only get top 100 rows
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])

            log("houseTable] Data pulled: " + str(data), "INFO")
        except Exception as e:
            log("[houseTable] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                    "statusCode": 500,
                    "message": "Error interacting with DB"
                })
            )
        finalData = []
        for item in data:
            if "min_amount" in self._validatedRequest and "max_amount" in self._validatedRequest:
                if not (int(item["price"]) >= int(self._validatedRequest["min_amount"]) and \
                    int(item["price"]) <= int(self._validatedRequest["max_amount"])):
                    continue
            if "min_bedroom" in self._validatedRequest and "max_bedroom" in self._validatedRequest:
                if not (int(item["no_of_rooms"]) >= int(self._validatedRequest["min_bedroom"]) and \
                    int(item["no_of_rooms"]) <= int(self._validatedRequest["max_bedroom"])):
                    continue
            if "min_bathroom" in self._validatedRequest and "max_bathroom" in self._validatedRequest:
                if not (int(item["no_of_toilets"]) >= int(self._validatedRequest["min_bathroom"]) and \
                    int(item["no_of_toilets"]) <= int(self._validatedRequest["max_bathroom"])):
                    continue
            if "min_sqfeet" in self._validatedRequest and "max_sqfeet" in self._validatedRequest:
                if not (int(item["square_feet"]) >= int(self._validatedRequest["min_sqfeet"]) and \
                    int(item["square_feet"]) <= int(self._validatedRequest["max_sqfeet"])):
                    continue
            if "type" in self._validatedRequest:
                if item["type"] != self._validatedRequest["type"] and self._validatedRequest["type"] != "All":
                    continue
            finalData.append(item)
        return finalData

    def getRecommendationBasedOnFilter(self):
        self._dat = self.retrievePageFromArray(self.getHouseDataFilter(), int(self._validatedRequest["page"]))
        

    
    
    def retrievePageFromArray(self, data, page):
        page -= 1 
        startingPage = 0 #starting element in data
        endingPage = self._paginationSize - 1 #ending element in data
        if startingPage + page * int(self._paginationSize) > len(data) - 1: #limiting start of page to valid index, return nothing if not valid
            return []
        if endingPage + page * int(self._paginationSize) > len(data) - 1: #limiting end of page to valid index, if less than what we want, return only a certain number
            data[startingPage + int(page) * int(self._paginationSize): len(data) + 1]
        return data[startingPage + page * int(self._paginationSize): endingPage + page * int(self._paginationSize) + 1] #return the full amount
    
    def buildResponse(self):
        if len(self._dat) == 0:
            log("[Pagination] Page empty.", "ERROR")
            raise Exception(json.dumps({
                    "statusCode": 404,
                    "message": "No more page"
                })
            )
        else:
            return {
                "statusCode": 200,
                "body": {
                    "houses": self._dat
                }
            }
    def getCompany(self):
        try:
            table = dynamodb.Table(self._companyTableName)

            response = table.scan()
            data = response['Items']
            #this is internal pagination, scan can only get top 100 rows
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])

            log("[companyTable] Data pulled: " + str(data), "INFO")
            companies = {}
            for i in data:
                company_id = i["company_id"]
                del i["company_id"]
                i["company_address"] = i["address"]
                del i["address"]
                i["company_type"] = i["type"]
                del i["type"]
                companies[company_id] = i
            
            for i,v in enumerate(self._dat):
                self._dat[i] = {**self._dat[i], **companies[self._dat[i]["company_id"]]}
        except Exception as e:
            log("[companyTable] Failed.", "ERROR", e)
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
