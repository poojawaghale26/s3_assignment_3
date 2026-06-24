import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from awsglue.utils import getResolvedOptions


# Read job arguments
args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "SOURCE_BUCKET",
        "TARGET_BUCKET",
        "object_key"
    ]
)

source_bucket = args["SOURCE_BUCKET"]
target_bucket = args["TARGET_BUCKET"]
object_key = args["object_key"]


# Spark Session
spark = (
    SparkSession.builder
    .appName("CSVSmallJob")
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
    f"Reading CSV file from "
    f"{input_path}"
)


# Read CSV
df = (
    spark.read
    .option("header", "true")
    .csv(input_path)
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
    f"Writing transformed file to "
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