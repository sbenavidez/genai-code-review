import boto3
from botocore.exceptions import ClientError

def scan_dynamodb_table(table_name, filter_expression=None, expression_values=None):
    """
    Scans a DynamoDB table and retrieves items...

    Parameters:
    - table_name (str): The name of the DynamoDB table to scan.
    - filter_expression (str, optional): A condition expression to filter items.
    - expression_values (dict, optional): A dictionary of values for placeholders in the filter expression.

    Returns:
    - list: A list of items from the DynamoDB table.
    - None: If an error occurs during the scan operation.
    """
    # Initialize a DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    try:
        # Reference the DynamoDB tabless
        table = dynamodb.Table(table_name)

        # Prepare scan arguments
        scan_kwargs = {}
        if filter_expression and expression_values:
            scan_kwargs['FilterExpression'] = filter_expression
            scan_kwargs['ExpressionAttributeValues'] = expression_values

        # Perform the scan operation
        response = table.scan(**scan_kwargs)

        # Collect all items (handle pagination if necessary)
        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = table.scan(**scan_kwargs)
            items.extend(response.get('Items', []))

        return items

    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return None

# Example usage
if __name__ == "__main__":
    # Define the table name
    table_name = "YourDynamoDBTable"

    # Optional filter example: Filter items where "attribute1" equals "value1"
    filter_expression = "attribute1 = :val1"
    expression_values = {":val1": "value1"}

    # Scan the table
    results = scan_dynamodb_table(table_name, filter_expression, expression_values)

    if results:
        print(f"Retrieved {len(results)} items:")
        for item in results:
            print(item)
    else:
        print("No items found or an error occurred.")
