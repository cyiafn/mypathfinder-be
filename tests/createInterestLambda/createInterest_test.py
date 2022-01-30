import boto3
import json
import os
import pytest
from lambda_code.createInterest import lambda_function
from lambda_code.createInterest.lambda_function import RequestResponseProcessor


def test_createInterest1():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        validatedRequest = data["request"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._validatedRequest = validatedRequest
        rrp._email = email
        rrp.writeToDb()
        assert resp == rrp._response


def test_createInterest2():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_createInterest3():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test3.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_createInterest4():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test4.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_createInterest5():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test5.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_createInterest6():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test6.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_createInterest7():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test7.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_createInterest8():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test8.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        validatedRequest = data["request"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._validatedRequest = validatedRequest
        rrp._email = email
        rrp.writeToDb()
        assert resp == rrp._response

def test_createInterest9():
    testCaseDir = "./tests/createInterestLambda/testCases"
    os.environ["HOUSING_INTEREST_TABLE_NAME"] = "HousingInterest"
    os.environ["INSURANCE_INTEREST_TABLE_NAME"] = "InsuranceInterest"
    with open(testCaseDir + "/test9.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])