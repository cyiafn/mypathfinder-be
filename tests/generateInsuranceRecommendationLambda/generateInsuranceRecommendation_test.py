import boto3
import moto
import json
import os
import pytest
from lambda_code.generateInsuranceRecommendation import lambda_function
from decimal import Decimal




'''
Success test with filter
'''
def test_generateInsuranceRecommendation1():
    testCaseDir = "./tests/generateInsuranceRecommendationLambda/testCases"
    os.environ["COMPANY_TABLE_NAME"] = "Company"
    os.environ["PAGINATION_SIZE"] = "5"
    os.environ["USER_TABLE_NAME"] = "User"
    os.environ["INSURANCE_TABLE_NAME"] = "Insurance"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        req = lambda_function.lambda_handler(data["request"], {})
        res = data["response"]
        for plan in res["body"]["plans"]:
            for key, value in plan.items():
                if isinstance(value,int) or isinstance(value,float) or value.isdigit():
                    if key != "recommendation_id" and key != "contact_number":
                        plan[key] = Decimal(str(value))
        assert req == res

#fail
def test_generateInsuranceRecommendation2():
    testCaseDir = "./tests/generateInsuranceRecommendationLambda/testCases"
    os.environ["PAGINATION_SIZE"] = "5"
    os.environ["USER_TABLE_NAME"] = "User"
    os.environ["INSURANCE_TABLE_NAME"] = "Insurance"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


#no filter
def test_generateInsuranceRecommendation3():
    testCaseDir = "./tests/generateInsuranceRecommendationLambda/testCases"
    os.environ["PAGINATION_SIZE"] = "5"
    os.environ["USER_TABLE_NAME"] = "User"
    os.environ["INSURANCE_TABLE_NAME"] = "Insurance"
    with open(testCaseDir + "/test3.json") as json_file:
        data = json.load(json_file)
        rrq = lambda_function.RequestResponseProcessor({})
        rrq._email = data["email"]
        rrq.getRecommendationId()
        rrq._email = data["email"]
        rrq._validatedRequest["page"] = data["page"]
        rrq._userRecommendationId = "4"
        rrq.getRecommendationBasedOnId()
        res = rrq.buildResponse()
        rrq.getCompany()
        resActual = data["response"]
        for plan in resActual["body"]["plans"]:
            for key, value in plan.items():
                if isinstance(value,int) or isinstance(value,float) or value.isdigit():
                    if key != "recommendation_id" and key != "contact_number":
                        plan[key] = Decimal(str(value))
        assert resActual == res
