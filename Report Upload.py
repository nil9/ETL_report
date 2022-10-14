#!/usr/bin/env python

import glob
import boto3
import os
from botocore.client import Config

ACCESS_KEY_ID = 'AKIA4ZBZAM7E5AJSCWYM'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'reportcollectiontest'
FOLDER_NAME = 'uploaded_reports'


s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

csv_files = glob.glob(r"C:\Users\nilanjan.das\PycharmProjects\Generator_report\*.csv")
json_files = glob.glob(r"C:\Users\nilanjan.das\PycharmProjects\Generator_report\*.json")

for filename in csv_files:
    #print(filename)
    key = "%s/%s" % (FOLDER_NAME, os.path.basename(filename))
    print("Putting %s as %s" % (filename,key))
    s3.upload_file(filename, BUCKET_NAME, key)

for filename in json_files:
    key = "%s/%s" % (FOLDER_NAME, os.path.basename(filename))
    print("Putting %s as %s" % (filename,key))
    s3.upload_file(filename, BUCKET_NAME, key)

print("All_Done")

