import os
import boto3

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Perform image recognition using Amazon Rekognition
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}}
    )
    
    # Create a text representation of the recognition results
    labels_text = ''
    for label in response['Labels']:
        labels_text += f"Label: {label['Name']}, Confidence: {label['Confidence']}\n"
    
    # Upload the text representation back to the S3 bucket
    output_key = os.path.splitext(key)[0] + '_labels.txt'
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=labels_text.encode()
    )
    
    return {
        'statusCode': 200,
        'body': 'Recognition results stored'
    }
