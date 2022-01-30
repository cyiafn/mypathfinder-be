import boto3
import moto
import json
import os
import pytest
from lambda_code.processAnswers import lambda_function


'''
test functions MUST start with test_testname
These tests basically load data from the testCases folder and run it

on failure, you need to declare pytest raising an exception and check the exception message same or not (look at end of test_helloWorld2)
'''


def test_processAnswers1():
    testCaseDir = "./tests/processAnswersLambda/testCases"
    os.environ["RECOMMENDATION_TABLE_NAME"] = "Recommendation"
    os.environ["total_savings1"] = "120000"
    os.environ["total_savings2"] = "130000"
    os.environ["total_savings3"] = "140000"
    os.environ["total_savings4"] = "150000"
    os.environ["yearly_income1"] = "50000"
    os.environ["yearly_income2"] = "90000"
    os.environ["yearly_income3"] = "150000"
    os.environ["house_type1"] = "HDB"
    os.environ["house_type2"] = "Condo"
    os.environ["house_type3"] = "Landed"
    os.environ["house_valuation1"] = "3000000"
    os.environ["house_valuation2"] = "4000000"
    os.environ["house_valuation3"] = "5000000"
    os.environ["no_of_rooms1"] = "4"
    os.environ["no_of_rooms2"] = "5"
    with open(testCaseDir + "/test1.json") as json_file:
        data = json.load(json_file)
        assert json.loads(lambda_function.lambda_handler(
            data["request"], "")) == data["response"]


def test_processAnswers2():
    testCaseDir = "./tests/processAnswersLambda/testCases"
    os.environ["RECOMMENDATION_TABLE_NAME"] = "Recommendation"
    os.environ["total_savings1"] = "120000"
    os.environ["total_savings2"] = "130000"
    os.environ["total_savings3"] = "140000"
    os.environ["total_savings4"] = "150000"
    os.environ["yearly_income1"] = "50000"
    os.environ["yearly_income2"] = "90000"
    os.environ["yearly_income3"] = "150000"
    os.environ["house_type1"] = "HDB"
    os.environ["house_type2"] = "Condo"
    os.environ["house_type3"] = "Landed"
    os.environ["house_valuation1"] = "3000000"
    os.environ["house_valuation2"] = "4000000"
    os.environ["house_valuation3"] = "5000000"
    os.environ["no_of_rooms1"] = "4"
    os.environ["no_of_rooms2"] = "5"
    with open(testCaseDir + "/test2.json") as json_file:
        data = json.load(json_file)
        assert json.loads(lambda_function.lambda_handler(
            data["request"], "")) == data["response"]


def test_processAnswers3():
    testCaseDir = "./tests/processAnswersLambda/testCases"
    os.environ["RECOMMENDATION_TABLE_NAME"] = "Recommendation"
    os.environ["total_savings1"] = "120000"
    os.environ["total_savings2"] = "130000"
    os.environ["total_savings3"] = "140000"
    os.environ["total_savings4"] = "150000"
    os.environ["yearly_income1"] = "50000"
    os.environ["yearly_income2"] = "90000"
    os.environ["yearly_income3"] = "150000"
    os.environ["house_type1"] = "HDB"
    os.environ["house_type2"] = "Condo"
    os.environ["house_type3"] = "Landed"
    os.environ["house_valuation1"] = "3000000"
    os.environ["house_valuation2"] = "4000000"
    os.environ["house_valuation3"] = "5000000"
    os.environ["no_of_rooms1"] = "4"
    os.environ["no_of_rooms2"] = "5"
    with open(testCaseDir + "/test3.json") as json_file:
        data = json.load(json_file)
        assert json.loads(lambda_function.lambda_handler(
            data["request"], "")) == data["response"]


def test_processAnswers4():
    testCaseDir = "./tests/processAnswersLambda/testCases"
    os.environ["RECOMMENDATION_TABLE_NAME"] = "Recommendation"
    os.environ["total_savings1"] = "120000"
    os.environ["total_savings2"] = "130000"
    os.environ["total_savings3"] = "140000"
    os.environ["total_savings4"] = "150000"
    os.environ["yearly_income1"] = "50000"
    os.environ["yearly_income2"] = "90000"
    os.environ["yearly_income3"] = "150000"
    os.environ["house_type1"] = "HDB"
    os.environ["house_type2"] = "Condo"
    os.environ["house_type3"] = "Landed"
    os.environ["house_valuation1"] = "3000000"
    os.environ["house_valuation2"] = "4000000"
    os.environ["house_valuation3"] = "5000000"
    os.environ["no_of_rooms1"] = "4"
    os.environ["no_of_rooms2"] = "5"
    with open(testCaseDir + "/test4.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])


def test_processAnswers5():
    testCaseDir = "./tests/processAnswersLambda/testCases"
    os.environ["RECOMMENDATION_TABLE_NAME"] = "Recommendation"
    os.environ["total_savings1"] = "120000"
    os.environ["total_savings2"] = "130000"
    os.environ["total_savings3"] = "140000"
    os.environ["total_savings4"] = "150000"
    os.environ["yearly_income1"] = "50000"
    os.environ["yearly_income2"] = "90000"
    os.environ["yearly_income3"] = "150000"
    os.environ["house_type1"] = "HDB"
    os.environ["house_type2"] = "Condo"
    os.environ["house_type3"] = "Landed"
    os.environ["house_valuation1"] = "3000000"
    os.environ["house_valuation2"] = "4000000"
    os.environ["house_valuation3"] = "5000000"
    os.environ["no_of_rooms1"] = "4"
    os.environ["no_of_rooms2"] = "5"
    with open(testCaseDir + "/test5.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])

def test_processAnswers6():
    testCaseDir = "./tests/processAnswersLambda/testCases"
    os.environ["RECOMMENDATION_TABLE_NAME"] = "Recommendation"
    os.environ["total_savings1"] = "120000"
    os.environ["total_savings2"] = "130000"
    os.environ["total_savings3"] = "140000"
    os.environ["total_savings4"] = "150000"
    os.environ["yearly_income1"] = "50000"
    os.environ["yearly_income2"] = "90000"
    os.environ["yearly_income3"] = "150000"
    os.environ["house_type1"] = "HDB"
    os.environ["house_type2"] = "Condo"
    os.environ["house_type3"] = "Landed"
    os.environ["house_valuation1"] = "3000000"
    os.environ["house_valuation2"] = "4000000"
    os.environ["house_valuation3"] = "5000000"
    os.environ["no_of_rooms1"] = "4"
    os.environ["no_of_rooms2"] = "5"
    with open(testCaseDir + "/test6.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])

def test_processAnswers7():
    testCaseDir = "./tests/processAnswersLambda/testCases"
    os.environ["RECOMMENDATION_TABLE_NAME"] = "Recommendation"
    os.environ["total_savings1"] = "120000"
    os.environ["total_savings2"] = "130000"
    os.environ["total_savings3"] = "140000"
    os.environ["total_savings4"] = "150000"
    os.environ["yearly_income1"] = "50000"
    os.environ["yearly_income2"] = "90000"
    os.environ["yearly_income3"] = "150000"
    os.environ["house_type1"] = "HDB"
    os.environ["house_type2"] = "Condo"
    os.environ["house_type3"] = "Landed"
    os.environ["house_valuation1"] = "3000000"
    os.environ["house_valuation2"] = "4000000"
    os.environ["house_valuation3"] = "5000000"
    os.environ["no_of_rooms1"] = "4"
    os.environ["no_of_rooms2"] = "5"
    with open(testCaseDir + "/test7.json") as json_file:
        data = json.load(json_file)
        with pytest.raises(Exception) as execinfo:
            assert lambda_function.lambda_handler(
                data["request"], "") == Exception(data["response"])
