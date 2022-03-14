
import json
import os
import pytest
from lambda_code.getTransactions.lambda_function import lambda_handler


'''
Success test
'''
def test_getTransactions1():
    testCaseDir = "./tests/getTransactionsLambda/testCases"
    os.environ["PROVBE_TRANSACTION_TABLE_NAME"] = "provbe-Transaction"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        assert data["response"] == lambda_handler(data["request"], {})

'''
Validation test - missing required attribute
'''
def test_getTransactions2():
    testCaseDir = "./tests/getTransactionsLambda/testCases"
    os.environ["PROVBE_TRANSACTION_TABLE_NAME"] = "provbe-Transaction"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            lambda_handler(data["request"], {})
        assert json.loads(str(execinfo.value)) == data["response"]

'''
Validation test - extra attributes in request, more than what is expected from required and optional attributes
'''        
def test_getTransactions3():
    testCaseDir = "./tests/getTransactionsLambda/testCases"
    os.environ["PROVBE_TRANSACTION_TABLE_NAME"] = "provbe-Transaction"
    with open(testCaseDir + "/test3.json") as json_file:
        data = json.load(json_file)        
        with pytest.raises(Exception) as execinfo:
            lambda_handler(data["request"], {})
        assert json.loads(str(execinfo.value)) == data["response"]

'''
Validation test - multiple matches in a regex
'''        
def test_getTransactions4():
    testCaseDir = "./tests/getTransactionsLambda/testCases"
    os.environ["PROVBE_TRANSACTION_TABLE_NAME"] = "provbe-Transaction"
    with open(testCaseDir + "/test4.json") as json_file:
        data = json.load(json_file)        
        with pytest.raises(Exception) as execinfo:
            lambda_handler(data["request"], {})
        assert json.loads(str(execinfo.value)) == data["response"]

'''
Failure test - check lambda code: when will there be error interacting with db? (404)
'''
# def test_getTransactions5():
#     testCaseDir = "./tests/getTransactionsLambda/testCases"
#     os.environ["PROVBE_TRANSACTION_TABLE_NAME"] = "provbe-Transaction"
#     with open(testCaseDir + "/test5.json") as json_file:
#         data = json.load(json_file)
#         with pytest.raises(Exception) as execinfo:
#             lambda_handler(data["request"], {})
#         assert json.loads(str(execinfo.value)) == data["response"]