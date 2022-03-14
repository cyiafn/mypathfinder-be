
import json
import os
import pytest
from lambda_code.getListing.lambda_function import lambda_handler


'''
Success test
'''
def test_getListing1():
    testCaseDir = "./tests/getListingLambda/testCases"
    os.environ["LISTING_TABLE_NAME"] = "ProvBE-listing"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        assert data["response"] == lambda_handler(data["request"], {})

'''
Validation test - missing required attribute
'''
def test_getListing2():
    testCaseDir = "./tests/getListingLambda/testCases"
    os.environ["LISTING_TABLE_NAME"] = "ProvBE-listing"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            lambda_handler(data["request"], {})
        assert json.loads(str(execinfo.value)) == data["response"]

'''
Validation test - extra attributes in request, more than what is expected from required and optional attributes
'''        
def test_getListing3():
    testCaseDir = "./tests/getListingLambda/testCases"
    os.environ["LISTING_TABLE_NAME"] = "ProvBE-listing"
    with open(testCaseDir + "/test3.json") as json_file:
        data = json.load(json_file)        
        with pytest.raises(Exception) as execinfo:
            lambda_handler(data["request"], {})
        assert json.loads(str(execinfo.value)) == data["response"]

'''
Validation test - multiple matches in a regex
'''        
def test_getListing4():
    testCaseDir = "./tests/getListingLambda/testCases"
    os.environ["LISTING_TABLE_NAME"] = "ProvBE-listing"
    with open(testCaseDir + "/test4.json") as json_file:
        data = json.load(json_file)        
        with pytest.raises(Exception) as execinfo:
            lambda_handler(data["request"], {})
        assert json.loads(str(execinfo.value)) == data["response"]

'''
Failure test - non-existent fetch from db: tokenId not found
'''
def test_getListing5():
    testCaseDir = "./tests/getListingLambda/testCases"
    os.environ["LISTING_TABLE_NAME"] = "ProvBE-listing"
    with open(testCaseDir + "/test5.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            lambda_handler(data["request"], {})
        assert json.loads(str(execinfo.value)) == data["response"]