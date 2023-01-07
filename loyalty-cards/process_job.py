import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    dynamodb = boto3.client('dynamodb')

    try:
        for record in event['Records']:
            body = json.loads(record['body'])
            card_number = body['card_number']
            first_name = body['first_name']
            last_name = body['last_name']
            points = body['points']

            # Create a loyalty card in DynamoDB
            dynamodb.put_item(
                TableName='loyalty-cards',
                Item={
                    'card_number': {'S': card_number},
                    'first_name': {'S': first_name},
                    'last_name': {'S': last_name},
                    'points': {'N': points},
                }
            )
    except Exception as e:
        # Log the error message and send it to CloudWatch
        logger.exception(e)
        raise e
