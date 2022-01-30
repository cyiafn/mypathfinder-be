import boto3
import json
import os
import pytest
from lambda_code.createInterest import lambda_function
from lambda_code.generateLandingPageData.lambda_function import RequestResponseProcessor


def test_generateLandingPageData1():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData2():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        validatedRequest = data["Authorization"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._validatedRequest = validatedRequest
        with pytest.raises(Exception) as execinfo:
            assert rrp.readEmailFromCognito() == Exception(data["response"])


def test_generateLandingPageData3():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test3.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_generateLandingPageData4():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test4.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_generateLandingPageData5():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test5.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData6():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test6.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData7():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test7.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData8():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test8.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData9():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test9.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData10():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test10.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData11():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test11.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData12():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test12.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData13():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test13.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData14():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test14.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData15():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test15.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData16():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test16.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData17():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test17.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData18():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test18.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData19():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test19.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response


def test_generateLandingPageData20():
    testCaseDir = "./tests/generateLandingPageDataLambda/testCases"
    os.environ["USER_TABLE_NAME"] = "User"
    with open(testCaseDir + "/test20.json") as json_file:
        data = json.load(json_file)
        email = data["email"]
        resp = data["response"]

        rrp = RequestResponseProcessor({})
        rrp._email = email
        rrp.readDataFromDb()
        rrp.readFromApi()
        rrp.evaluateData()
        assert resp == rrp._response
