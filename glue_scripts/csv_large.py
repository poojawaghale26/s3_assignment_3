import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


# Read Glue Job Arguments
try:
    from awsglue.utils import getResolvedOptions

    args = getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "SOURCE_BUCKET",
            "TARGET_BUCKET",
            "object_key"
        ]
    )

except ImportError:
    # Local testing values
    args = {
        "JOB_NAME": "local-test",
        "SOURCE_BUCKET": "local-source",
        "TARGET_BUCKET": "local-target",
        "object_key": "sample.csv"
    }

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
    Convert country name to country code
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
    f"Reading CSV file from: "
    f"{input_path}"
)


# Read CSV File
df = (
    spark.read
    .option("header", "true")
    .csv(input_path)
)

record_count = df.count()

print(
    f"Total Records Read: "
    f"{record_count}"
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
    f"s3://{target_bucket}/csv/"
)

print(
    f"Writing transformed data to: "
    f"{output_path}"
)


# Write Output
(
    transformed_df.write
    .mode("append")
    .option("header", "true")
    .csv(output_path)
)

print(
    f"Successfully processed "
    f"{object_key}"
)

spark.stop()