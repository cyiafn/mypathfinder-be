import boto3
import moto
import json
import os
import pytest
from lambda_code.editProfile import lambda_function
from decimal import Decimal




'''
Success test with all values
'''
def test_editProfile1():
    testCaseDir = "./tests/editProfileLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        res = data["response"]
        req = data["request"]
        rrp = lambda_function.RequestResponseProcessor(req)
        rrp.validateRequest()
        rrp._email = data["email"]
        rrp.getProfile()
        rrp.reprocessAnswers()
        rrp.updateDb() 
        assert rrp.buildResponse() == res

'''
Validation test
'''
def test_editProfile2():
    testCaseDir = "./tests/editProfileLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])
        

'''
Failure test (nth to update)
'''
def test_editProfile3():
    testCaseDir = "./tests/editProfileLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])
        