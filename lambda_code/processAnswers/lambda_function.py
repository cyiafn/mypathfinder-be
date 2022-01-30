'''
This lambda function returns processed user data to 
the front end to generate personalised data landing page for the user
@author: Benjamin Ho

@request
RequiredAttributes = ["have_disability_insurance", "oa_saving", "no_of_room", "no_of_children", "have_critical_illness_insurance", "have_spouse",
                        "current_debt", "yearly_income", "current_saving", "house_valuation","have_hospitalisation_insurance", "house_type", "have_life_insurance"]
OptionalAttributes = []

@return
errorCode and message on fail
statusCode and body of recommendation_id on success
'''

import boto3
import json
import re
import boto3
import time
import datetime
import os
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
        self._points = 0
        self._unvalidatedRequest = event
        self._validatedRequest = {}
        self._recommendationTableName = os.environ["RECOMMENDATION_TABLE_NAME"]
        self._response = {
            "statusCode": 200,
            "body": {
                "recommendation_id": ""
            }
        }

    def orchestrate(self):
        '''
        Main orchestrating function
        '''
        self.validateRequest()
        self.calculatePoints()
        self.getRecId()
        return self._response

    def validateRequest(self):
        errorResponse = json.dumps({
            "statusCode": 400,
            "message": "Validation failed."
        })

        if (self._unvalidatedRequest["have_spouse"] != "true") and (self._unvalidatedRequest["have_spouse"] != "false"):
            log("[VALIDATION] Failed due to required Attributes incorrect.", "INFO")
            raise Exception(errorResponse)
        if (self._unvalidatedRequest["house_type"] != "HDB") and (self._unvalidatedRequest["house_type"] != "Condo") and (self._unvalidatedRequest["house_type"] != "Landed") and (self._unvalidatedRequest["house_type"] != ""):
            log("[VALIDATION] Failed due to required Attributes incorrect.", "INFO")
            raise Exception(errorResponse)
        if ((self._unvalidatedRequest["have_life_insurance"] != "true") and (self._unvalidatedRequest["have_life_insurance"] != "false")) or ((self._unvalidatedRequest["have_disability_insurance"] != "true") and (self._unvalidatedRequest["have_disability_insurance"] != "false")) or ((self._unvalidatedRequest["have_hospitalisation_insurance"] != "true") and (self._unvalidatedRequest["have_hospitalisation_insurance"] != "false")) or ((self._unvalidatedRequest["have_critical_illness_insurance"] != "true") and (self._unvalidatedRequest["have_critical_illness_insurance"] != "false")):
            log("[VALIDATION] Failed due to required Attributes incorrect.", "INFO")
            raise Exception(errorResponse)

        self._validatedRequest = self._unvalidatedRequest
        log("[VALIDATION] Success" + str(self._validatedRequest), "INFO")

    def calculatePoints(self):
        totalSavings = self._validatedRequest["oa_saving"] + \
            self._validatedRequest["current_saving"] + \
            self._validatedRequest["special_saving"]

        if totalSavings >= int(os.environ["total_savings4"]):
            self._points += 4
        elif totalSavings >= int(os.environ["total_savings3"]):
            self._points += 3
        elif totalSavings >= int(os.environ["total_savings2"]):
            self._points += 2
        elif totalSavings >= int(os.environ["total_savings1"]):
            self._points += 1

        if self._validatedRequest["yearly_income"] >= int(os.environ["yearly_income3"]):
            self._points += 3
        elif self._validatedRequest["yearly_income"] >= int(os.environ["yearly_income2"]):
            self._points += 2
        elif self._validatedRequest["yearly_income"] >= int(os.environ["yearly_income1"]):
            self._points += 1

        if self._validatedRequest["house_type"] != "":
            if self._validatedRequest["house_type"] == os.environ["house_type1"]:
                self._points += 1
            elif self._validatedRequest["house_type"] == os.environ["house_type2"]:
                self._points += 2
            else:
                self._points += 3

            if int(self._validatedRequest["no_of_room"]) >= int(os.environ["no_of_rooms2"]):
                self._points += 2
            elif int(self._validatedRequest["no_of_room"]) >= int(os.environ["no_of_rooms1"]):
                self._points += 1

            if self._validatedRequest["house_valuation"] >= int(os.environ["house_valuation3"]):
                self._points += 3
            elif self._validatedRequest["house_valuation"] >= int(os.environ["house_valuation2"]):
                self._points += 2
            elif self._validatedRequest["house_valuation"] >= int(os.environ["house_valuation1"]):
                self._points += 1

        if self._validatedRequest["current_debt"] > 0:
            self._points -= 1

        if self._validatedRequest["have_spouse"] == "true":
            self._points -= 1

        if self._validatedRequest["no_of_children"] != 0:
            self._points -= self._validatedRequest["no_of_children"]

        if self._validatedRequest["have_life_insurance"] == "true":
            self._points += 1

        if self._validatedRequest["have_disability_insurance"] == "true":
            self._points += 1

        if self._validatedRequest["have_hospitalisation_insurance"] == "true":
            self._points += 1

        if self._validatedRequest["have_critical_illness_insurance"] == "true":
            self._points += 1

    def getRecId(self):
        try:
            table = dynamodb.Table(self._recommendationTableName)
            response = table.scan(
                FilterExpression=Attr("max_point").gt(
                    self._points) & Attr("min_point").lte(self._points)
            )
            data = response['Items']

            log("RecommendationDB] Data pulled: " + str(data), "INFO")
        except Exception as e:
            log("[RecommendationDB] Failed.", "ERROR", e)
            raise Exception(json.dumps({
                "statusCode": 500,
                "message": "Error interacting with DB"
            })
            )
        self._response = {
            "recommendation_id": str(data[0]["recommendation_id"])
        }


def lambda_handler(event, context):
    req = RequestResponseProcessor(event)
    res = req.orchestrate()
    log("[RESPONSE] " + str(res), "INFO")
    return json.dumps(res)
