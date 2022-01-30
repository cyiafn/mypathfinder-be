import pytest
import moto
import boto3
import json
import os
from decimal import Decimal

dbPath = "tests/sampleData"
dbSchemaPath = "tests/dbSchema"

#global fixture for setup and teardown of tests
@pytest.fixture(scope="session", autouse=True)
def setup():
    print("\nBuilding mock db.")
    with moto.mock_dynamodb2():
        dynamodb = boto3.resource('dynamodb')
        createTable(dynamodb)
        yield dynamodb
        cleanUpDB(dynamodb)

#creating the tables with proper schemas
def createTable(dynamodb):
    files = [f for f in os.listdir(dbSchemaPath)]
    for f in files:
        with open(dbSchemaPath + "/" + f) as json_file:
            data = json.load(json_file)["Table"]
            table_name = data["TableName"]
            if "GlobalSecondaryIndexes" in data:
                table = dynamodb.create_table(TableName=table_name,
                    KeySchema=data["KeySchema"],
                    AttributeDefinitions=data["AttributeDefinitions"],
                    GlobalSecondaryIndexes=data["GlobalSecondaryIndexes"],
                    BillingMode='PAY_PER_REQUEST')
            else:
                table = dynamodb.create_table(TableName=table_name,
                    KeySchema=data["KeySchema"],
                    AttributeDefinitions=data["AttributeDefinitions"],
                    BillingMode='PAY_PER_REQUEST')
            
            populateTable(table, table_name)

#populating tables
def populateTable(table, tableName):
    if os.path.isfile(dbPath + "/" + tableName + ".json"):
        with open(dbPath + "/" + tableName + ".json") as json_file:
            data = json.load(json_file)["Items"]
            with table.batch_writer() as batch:
                for row in data:
                    finalQuery = {}
                    for key, val in row.items():
                        if "S" in val:
                            finalQuery[key] = str(val["S"])
                        elif "N" in val:
                            finalQuery[key] = Decimal(val["N"])
                    table.put_item(Item = finalQuery)
    else:
        print("No sample data found for table: "+ tableName)

#cleaning up (removing all tables)
def cleanUpDB(dynamodb):
    files = [f for f in os.listdir(dbSchemaPath)]
    for f in files:
        f = f.replace(".json", "")
        table = dynamodb.Table(f)
        table.delete()
            


if __name__ == "__main__":
    populateTable("test", "helloWorldTable")