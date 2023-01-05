import json
import boto3

client = boto3.client('dynamodb')


def handler(event, context):
    try:
        data = client.scan(
            TableName='loyalty-cards'
        )

        items = data['Items']

        response = {
            'statusCode': 200,
            'body': json.dumps({
                'items': items,
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'An error occurred',
                'error': str(e),
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

    return response
