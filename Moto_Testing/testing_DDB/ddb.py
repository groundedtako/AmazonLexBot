import boto3


class MyDDBClient:
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client("dynamodb", region_name=region_name)

    def list_tables(self):
        """Return a list of tables"""
        response = self.client.list_tables()
        print("\nListing All DynamoDB tables: ")
        tables = [TableName for TableName in response["TableNames"]]
        print(tables)
        print("-------------------")
        return tables

    def create_ddb_table(self):
        table_rsp = self.client.create_table(
            TableName = "testing_table",
            KeySchema=[
                    {
                        'AttributeName': 'RecordId',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'RecordId',
                        'AttributeType': 'S'
                    },
                ],
                BillingMode='PAY_PER_REQUEST'
            )
        return table_rsp


