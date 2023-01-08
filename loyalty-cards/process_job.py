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
            created_at = body['created_at']

            # Check if the user already exists in the database
            response = dynamodb.get_item(
                TableName='loyalty-cards',
                Key={
                    'card_number': {'S': card_number},
                }
            )
            if 'Item' in response:
                # User already exists, add the current points to the incoming points
                item = response['Item']

                # Add the points from the incoming message to the existing points
                points = int(item['points']['N']) + int(points)

            # Create or update the loyalty card in DynamoDB
            dynamodb.put_item(
                TableName='loyalty-cards',
                Item={
                    'card_number': {'S': card_number},
                    'first_name': {'S': first_name},
                    'last_name': {'S': last_name},
                    'points': {'N': points},
                    'created_at': {'S': created_at},
                }
            )
    except Exception as e:
        # Log the error message and send it to CloudWatch
        logger.exception(e)
        raise e
