import random
import boto3
import json
import datetime

client = boto3.client('dynamodb')


def generate_number():
    return "8880" + "".join(str(random.randint(0, 9)) for _ in range(12))


def handler(event, context):
    # Parse the request body as JSON
    body = json.loads(event['body'])

    # Check if the request includes the first_name and last_name fields
    if 'first_name' not in body or 'last_name' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing required fields'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

    try:
        current_time = str(datetime.datetime.now())
        card_number = generate_number()

        # Get the first_name and last_name from the request
        first_name = body['first_name']
        last_name = body['last_name']

        client.put_item(
            TableName='loyalty-cards',
            Item={
                'card_number': {'S': card_number},
                'first_name': {'S': first_name},
                'last_name': {'S': last_name},
                'points': {'N': '0'},  # Set points to 0
                'created_at': {'S': current_time},
            }
        )

        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Card created successfully',
                'data': {
                    'card_number': card_number,
                    'first_name': first_name,
                    'last_name': last_name,
                    'points': 0,
                    'created_at': current_time,
                },
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
