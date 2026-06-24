import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from awsglue.utils import getResolvedOptions


# Read Glue Job Arguments
args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "SOURCE_BUCKET",
        "TARGET_BUCKET",
        "object_key"
    ]
)

job_name = args["JOB_NAME"]
source_bucket = args["SOURCE_BUCKET"]
target_bucket = args["TARGET_BUCKET"]
object_key = args["object_key"]


# Create Spark Session
spark = (
    SparkSession.builder
    .appName(job_name)
    .getOrCreate()
)


# Country Mapping Dictionary
COUNTRY_CODE_MAPPING = {
    "India": "IN",
    "United States": "US",
    "Canada": "CA",
    "Australia": "AU",
    "Germany": "DE",
    "France": "FR",
    "Japan": "JP",
    "China": "CN"
}


def get_country_code(country):
    """
    Return country code from mapping.
    """

    return COUNTRY_CODE_MAPPING.get(
        country,
        "UNKNOWN"
    )


country_code_udf = udf(
    get_country_code,
    StringType()
)


# Source File Path
input_path = (
    f"s3://{source_bucket}/{object_key}"
)

print(
    f"Reading file from: {input_path}"
)


# Read CSV File
df = (
    spark.read
    .option("header", "true")
    .csv(input_path)
)

print(
    f"Total Records Read: {df.count()}"
)


# Add country_code Column
transformed_df = (
    df.withColumn(
        "country_code",
        country_code_udf(df["country"])
    )
)


# Output Path
output_path = (
    f"s3://{target_bucket}/csv/"
)

print(
    f"Writing output to: {output_path}"
)


# Write Transformed Data
(
    transformed_df.write
    .mode("append")
    .option("header", "true")
    .csv(output_path)
)

print(
    f"Successfully processed file: {object_key}"
)

spark.stop()