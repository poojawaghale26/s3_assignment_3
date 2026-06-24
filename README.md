# s3_assignment_3

AWS Event Driven Data Pipeline

Workflow:

1. File uploaded to SourceBucket.
2. S3 event triggers SNS Topic.
3. SNS invokes:
   - LambdaSaveS3Config
   - LambdaRunGlueJob
4. LambdaSaveS3Config stores object metadata in DynamoDB.
5. LambdaRunGlueJob reads metadata and starts appropriate Glue Job.
6. Glue Job transforms file and writes output to CrawlerBucket.
7. EventBridge listens for Glue Job state changes.
8. On SUCCESS:
   - LambdaGlueJobSuccess runs.
   - Starts appropriate crawler.
   - Waits for crawler completion.
   - Executes Athena query.
   - Saves output to AthenaOutputBucket.
9. On FAILURE:
   - LambdaGlueJobFailure runs.
   - Sends alert through SNS email notification.
10. All resources are deployed using CloudFormation and deploy.py.
