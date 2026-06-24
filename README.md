AWS Event-Driven Data Processing Pipeline
Overview

This project implements an event-driven AWS data processing pipeline using AWS Lambda, S3, SNS, DynamoDB, Glue, EventBridge, Athena, and CloudFormation.

When a file is uploaded to the Source S3 Bucket, the pipeline automatically:

Stores file metadata in DynamoDB.
Selects and runs an appropriate Glue Job based on file type and size.
Transforms the input data.
Stores transformed data in a crawler bucket.
Runs a Glue Crawler after successful Glue Job execution.
Creates/updates Glue Catalog tables.
Executes Athena queries on the generated tables.
Stores Athena query results in an output bucket.
Sends email notifications if a Glue Job fails.
Architecture
SourceBucket
     |
     v
S3 Event Notification
     |
     v
SNS Topic
   /     \
  /       \
 v         v

LambdaSaveS3Config      LambdaRunGlueJob
       |                       |
       v                       |
 DynamoDB Table <--------------|
                               |
                               v
                         Glue Job
                               |
                               v
                        CrawlerBucket
                               |
                  +------------+------------+
                  |                         |
                  v                         v

         EventBridge Success       EventBridge Failure
                  |                         |
                  v                         v

      LambdaGlueJobSuccess     LambdaGlueJobFailure
                  |                         |
                  v                         |
           Run Crawler                      |
                  |                         |
                  v                         |
           Glue Database                    |
                  |                         |
                  v                         |
            Athena Query                    |
                  |                         |
                  v                         |
       Athena Output Bucket          SNS Email Alert
AWS Services Used
Amazon S3
AWS Lambda
Amazon SNS
Amazon DynamoDB
AWS Glue Jobs
AWS Glue Crawlers
Amazon EventBridge
Amazon Athena
AWS IAM
AWS CloudFormation
Project Structure
aws-data-pipeline/
│
├── deploy.py
├── cf_template.yaml
├── README.md
│
├── lambda/
│   ├── save_s3_config/
│   │   └── handler.py
│   │
│   ├── run_glue_job/
│   │   └── handler.py
│   │
│   ├── glue_success/
│   │   └── handler.py
│   │
│   └── glue_failure/
│       └── handler.py
│
├── glue_scripts/
│   ├── csv_small.py
│   ├── csv_medium.py
│   ├── csv_large.py
│   ├── json_small.py
│   ├── json_medium.py
│   ├── json_large.py
│   ├── text_small.py
│   ├── text_medium.py
│   └── text_large.py
│
├── shared/
│   ├── constants.py
│   ├── logger.py
│   └── utils.py
│
└── tests/
Workflow
Step 1: File Upload

A file is uploaded to the SourceBucket.

Example:

employee.csv
Step 2: SNS Notification

S3 event notification publishes the event to SNS Topic.

SNS fan-outs the event to:

LambdaSaveS3Config
LambdaRunGlueJob
Step 3: Save File Metadata

LambdaSaveS3Config extracts:

Object Key
Version ID
Content Type
File Size
Last Modified Date
Metadata
Tags

and stores them in DynamoDB.

Example Item:

{
  "object_key": "employee.csv",
  "content_type": "csv",
  "file_size": 6000,
  "version_id": "123abc"
}
Step 4: Select Glue Job

LambdaRunGlueJob reads metadata from DynamoDB.

Glue Job selection logic:

CSV Files
File Size	Glue Job
0 - 5 KB	CSVSmallJob
5 - 10 KB	CSVMediumJob
> 10 KB	CSVLargeJob
JSON Files
File Size	Glue Job
0 - 5 KB	JSONSmallJob
5 - 10 KB	JSONMediumJob
> 10 KB	JSONLargeJob
TEXT Files
File Size	Glue Job
0 - 5 KB	TextSmallJob
5 - 10 KB	TextMediumJob
> 10 KB	TextLargeJob

Total Glue Jobs: 9

Step 5: Data Transformation

Input:

name,age,country
John,30,India
Sam,40,USA

Transformation:

country_mapping = {
    "India": "IN",
    "USA": "US"
}

Output:

name,age,country,country_code
John,30,India,IN
Sam,40,USA,US

Output is written to:

CrawlerBucket
Step 6: Glue Job Success

EventBridge detects Glue Job SUCCESS.

LambdaGlueJobSuccess:

Identifies Glue Job.
Runs corresponding Crawler.
Waits until crawler completes.
Executes Athena query.

Example:

SELECT * FROM csv_table;

Athena results are stored in:

AthenaOutputBucket
Step 7: Glue Job Failure

EventBridge detects Glue Job FAILURE.

LambdaGlueJobFailure publishes a message to SNS Topic Output.

SNS sends email notification.

Example:

Subject: Glue Job Failed

Message:
CSVMediumJob failed for employee.csv
Deployment
Prerequisites
Python 3.10+
AWS CLI configured
Boto3 installed
Appropriate IAM permissions

Install dependencies:

pip install boto3
Deploy Infrastructure

Run:

python deploy.py

Deployment steps:

Create Code Bucket
Package Lambda Functions
Upload Lambda ZIP files
Upload Glue Scripts
Deploy CloudFormation Stack
Resiliency Features
SNS Fan-Out

Multiple Lambda functions can consume the same S3 event independently.

Idempotency

Unique processing key:

object_key + version_id

Prevents duplicate processing.

DynamoDB Tracking

Stores processing status and metadata.

EventBridge Monitoring

Eliminates polling and provides reliable Glue Job state notifications.

Dead Letter Queue (Recommended)

Failed Lambda events can be routed to DLQ for reprocessing.

SQS Buffering (Recommended)

For high-volume concurrent uploads:

S3 → SNS → SQS → Lambda

This prevents message loss and throttling.

Expected Output
File Uploaded: employee.csv

Metadata Saved Successfully

Selected Glue Job:
CSVMediumJob

Glue Job Started

Glue Job SUCCEEDED

CSVFilesCrawler Started

CSVFilesCrawler Completed

Athena Query Executed

Results Saved To AthenaOutputBucket

Failure scenario:

Glue Job FAILED

SNS Notification Sent

Email Alert Delivered
Author

AWS Event-Driven Data Processing Pipeline Assignment

Implemented using:

Python
Boto3
AWS Lambda
AWS Glue
DynamoDB
Athena
SNS
EventBridge
CloudFormation