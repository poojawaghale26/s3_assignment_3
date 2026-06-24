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


# Country Mapping
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
    Return country code for country name.
    """
    return COUNTRY_CODE_MAPPING.get(
        country,
        "UNKNOWN"
    )


country_code_udf = udf(
    get_country_code,
    StringType()
)


# Input Path
input_path = (
    f"s3://{source_bucket}/{object_key}"
)

print(
    f"Reading JSON file from: "
    f"{input_path}"
)


# Read JSON
df = spark.read.json(input_path)

print(
    f"Total Records Read: "
    f"{df.count()}"
)


# Add country_code column
transformed_df = (
    df.withColumn(
        "country_code",
        country_code_udf(df["country"])
    )
)


# Output Path
output_path = (
    f"s3://{target_bucket}/json/"
)

print(
    f"Writing transformed data to: "
    f"{output_path}"
)


# Write JSON Output
(
    transformed_df.write
    .mode("append")
    .json(output_path)
)

print(
    f"Successfully processed "
    f"{object_key}"
)

spark.stop()