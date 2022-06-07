import os
import boto3

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_TOKEN = os.getenv("SESSION_TOKEN")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def create_file_in_bucket(content, file_path):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=SESSION_TOKEN
    )
    s3.Object(BUCKET_NAME, file_path).put(Body=content)
