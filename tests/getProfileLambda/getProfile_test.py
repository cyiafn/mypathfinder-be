import boto3
import moto
import json
import os
import pytest
from lambda_code.getProfile.lambda_function import RequestResponseProcessor
from decimal import Decimal




'''
Success test
not possible to fail
'''
def test_getProfile1():
    testCaseDir = "./tests/getProfileLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test1.json") as json_file:
       
        data = json.load(json_file)
        print(data)
        email = data["email"]
        res = data["response"]
        for key, value in res["body"].items():
            if isinstance(value,int) or isinstance(value,float) or value.isdigit():
                res["body"][key] = Decimal(str(value))
        
        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.getProfile()
        
        assert res == rrp.buildResponse()

