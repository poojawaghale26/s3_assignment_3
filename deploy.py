import boto3
import os
import zipfile
from botocore.exceptions import ClientError

# Configuration
REGION = "us-east-1"
STACK_NAME = "DataPipelineStack"
CODE_BUCKET = "my-data-pipeline-code-bucket"
TEMPLATE_FILE = "cf_template.yaml"

s3 = boto3.client("s3", region_name=REGION)
cf = boto3.client("cloudformation", region_name=REGION)


class S3Manager:
    def create_bucket(self):
        try:
            s3.head_bucket(Bucket=CODE_BUCKET)
            print(f"Bucket {CODE_BUCKET} already exists")
        except:
            print(f"Creating bucket {CODE_BUCKET}")
            s3.create_bucket(Bucket=CODE_BUCKET)

    def upload_file(self, local_path, s3_key):
        print(f"Uploading {local_path}")
        s3.upload_file(local_path, CODE_BUCKET, s3_key)


class ZipManager:
    @staticmethod
    def zip_folder(folder_path, zip_name):
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arc_name)

        return zip_name


#from botocore.exceptions import ClientError

from botocore.exceptions import ClientError

class CloudFormationManager:
    
    def deploy_stack(self):

        with open(TEMPLATE_FILE, "r") as f:
            template_body = f.read()

        cf.validate_template(
            TemplateBody=template_body
        )

        print("Template validation successful")

        parameters = [
            {
                "ParameterKey": "SourceBucketName",
                "ParameterValue": "my-source-bucket-243050854856"
            },
            {
                "ParameterKey": "CrawlerBucketName",
                "ParameterValue": "my-crawler-bucket-243050854856"
            },
            {
                "ParameterKey": "AthenaOutputBucketName",
                "ParameterValue": "my-athena-output-bucket-243050854856"
            }
        ]

        try:
            cf.describe_stacks(StackName=STACK_NAME)

            print("Stack exists. Updating stack...")

            cf.update_stack(
                StackName=STACK_NAME,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=["CAPABILITY_NAMED_IAM"]
            )

            print("Stack update started")
            return True

        except ClientError as e:

            error_message = str(e)

            print("Actual Error:")
            print(error_message)

            if "does not exist" in error_message:

                print("Creating stack...")

                cf.create_stack(
                    StackName=STACK_NAME,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=["CAPABILITY_NAMED_IAM"]
                )

                print("Stack creation started")
                return True

            elif "ROLLBACK_COMPLETE" in error_message:

                print("Deleting failed stack...")

                cf.delete_stack(StackName=STACK_NAME)

                waiter = cf.get_waiter("stack_delete_complete")
                waiter.wait(StackName=STACK_NAME)

                print("Creating stack again...")

                cf.create_stack(
                    StackName=STACK_NAME,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=["CAPABILITY_NAMED_IAM"]
                )

                print("Stack recreation started")
                return True

            elif "No updates are to be performed" in error_message:

                print("No changes detected")
                return True

            else:
                raise e

        return True

def upload_lambda_packages(s3_manager):
    lambdas_folders = [
        "lambda/save_s3_config",
        "lambda/run_glue_job",
        "lambda/glue_success",
        "lambda/glue_failure"
    ]

    for folder in lambdas_folders:
        zip_name = folder.split("/")[-1] + ".zip"

        ZipManager.zip_folder(folder, zip_name)

        s3_manager.upload_file(
            zip_name,
            f"lambda/{zip_name}"
        )


def upload_glue_scripts(s3_manager):
    glue_folder = "glue_scripts"

    for file in os.listdir(glue_folder):
        file_path = os.path.join(glue_folder, file)

        if os.path.isfile(file_path):
            s3_manager.upload_file(
                file_path,
                f"glue_scripts/{file}"
            )


def main():
    s3_manager = S3Manager()
    cf_manager = CloudFormationManager()

    print("Step 1: Create code bucket")
    s3_manager.create_bucket()

    print("Step 2: Upload lambda packages")
    upload_lambda_packages(s3_manager)

    print("Step 3: Upload glue scripts")
    upload_glue_scripts(s3_manager)

    print("Step 4: Deploy cloudformation stack")
    success = cf_manager.deploy_stack()

    if success:
        print("Deployment completed successfully")
    else:
        print("Deployment failed")

if __name__ == "__main__":
    main()