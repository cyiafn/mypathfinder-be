import boto3
import moto
import json
import os
import pytest
from lambda_code.generateHousingRecommendation import lambda_function
from decimal import Decimal




'''
Success test with filter
'''
def test_generateHousingRecommendation1():
    testCaseDir = "./tests/generateHousingRecommendationLambda/testCases"
    os.environ["COMPANY_TABLE_NAME"] = "Company"
    os.environ["PAGINATION_SIZE"] = "5"
    os.environ["USER_TABLE_NAME"] = "User"
    os.environ["HOUSING_TABLE_NAME"] = "House"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        req = lambda_function.lambda_handler(data["request"], {})
        res = data["response"]
        for house in res["body"]["houses"]:
            for key, value in house.items():
                if isinstance(value,int) or isinstance(value,float) or value.isdigit():
                    if key != "house_recommendation_id" and key != "contact_number":
                        house[key] = Decimal(str(value))
        assert req == res

def test_generateHousingRecommendation2():
    testCaseDir = "./tests/generateHousingRecommendationLambda/testCases"
    os.environ["COMPANY_TABLE_NAME"] = "Company"
    os.environ["PAGINATION_SIZE"] = "5"
    os.environ["USER_TABLE_NAME"] = "User"
    os.environ["HOUSING_TABLE_NAME"] = "House"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])

def test_generateHousingRecommendation3():
    testCaseDir = "./tests/generateHousingRecommendationLambda/testCases"
    os.environ["PAGINATION_SIZE"] = "5"
    os.environ["USER_TABLE_NAME"] = "User"
    os.environ["HOUSING_TABLE_NAME"] = "House"
    os.environ["COMPANY_TABLE_NAME"] = "Company"
    with open(testCaseDir + "/test3.json") as json_file:
        data = json.load(json_file)
        rrq = lambda_function.RequestResponseProcessor({})
        rrq._email = data["email"]
        rrq.getRecommendationId()
        rrq._email = data["email"]
        rrq._validatedRequest["page"] = data["page"]
        rrq._userRecommendationId = "4"
        rrq.getRecommendationBasedOnId()
        rrq.getCompany()
        res = rrq.buildResponse()
        resActual = data["response"]
        for house in resActual["body"]["houses"]:
            for key, value in house.items():
                if isinstance(value,int) or isinstance(value,float) or value.isdigit():
                    if key != "house_recommendation_id" and key != "contact_number":
                        house[key] = Decimal(str(value))
        assert resActual == res
