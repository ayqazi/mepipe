#!/usr/bin/env python
import os
import sys

import boto3
from botocore.config import Config
import requests

media_id = "deadbeef"
key = "test-upload.data"
bucket = "com-cloudership-eu-west-1-frootube-video-upload"
# bucket = "a1b1-playground-scratch"

s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
response = s3.generate_presigned_post(
    Bucket=bucket,
    Key=key,
    ExpiresIn=3600,
    Fields={
        'x-amz-meta-id': media_id,
    },
    Conditions=[
        {'x-amz-meta-id': media_id},
    ]
)

print("presigned post response")
print(response)

# file = "test/testdata/test-video.mp4"
file = sys.argv[1]

curl_fields = ' '.join([f"-F '{k}={v}'" for k, v in response['fields'].items()])
print(f"curl -vv {curl_fields} -F 'file=@{file}' -L {response['url']}")

# with open(file, "rb") as f:
#     files = {"file": (key, f)}
#     http_response = requests.post(response['url'], data=response['fields'], files=files)
#
# print(http_response)
