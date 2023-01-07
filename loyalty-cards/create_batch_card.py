import boto3
import csv
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/501968831602/loyalty-card-queue'

    try:
        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')

        # Read the CSV file and create a job for each line
        reader = csv.DictReader(content.splitlines())
        for row in reader:
            job = {
                'card_number': row['card_number'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'points': row['points'],
            }
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(job))
    except Exception as e:
        # Log the error message and send it to CloudWatch
        logger.exception(e)
        raise e
