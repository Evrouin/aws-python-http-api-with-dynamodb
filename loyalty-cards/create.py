import random
import boto3
import json
import datetime

client = boto3.client('dynamodb')


def generate_number():
    return "8880" + "".join(str(random.randint(0, 9)) for _ in range(12))


def handler(event, context):
    try:
        current_time = str(datetime.datetime.now())
        card_number = generate_number()

        client.put_item(
            TableName='loyalty-cards',
            Item={
                'card_number': {'S': card_number},
                'created_at': {'S': current_time},
            }
        )

        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Card created successfully',
                'data': {
                    'card_number': card_number,
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
