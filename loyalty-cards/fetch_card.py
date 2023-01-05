import boto3
import json
import time

client = boto3.client('dynamodb')


def handler(event, context):
    try:
        card_number = event['pathParameters']['card_number']

        response = client.get_item(
            TableName='loyalty-cards',
            Key={
                'card_number': {'S': card_number}
            }
        )

        if 'Item' not in response:
            raise Exception('Card number not found')

        item = response.get('Item', {})
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Card retrieved successfully',
                'data': item,
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
    except Exception as e:
        return {
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
