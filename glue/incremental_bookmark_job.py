"""
AWS Glue PySpark example: incremental S3-to-S3 load with job bookmarks.

Expected Glue job parameters:
  --SOURCE_DATABASE  Glue Data Catalog database containing the source table
  --SOURCE_TABLE     Glue Data Catalog table for incoming order data
  --TARGET_PATH      s3://<bucket>/<prefix>/curated/orders/

Enable bookmarks in the Glue job settings or pass:
  --job-bookmark-option job-bookmark-enable

The source table should expose an order_date field suitable for partitioning.
Adapt the schema, catalog names and target layout to your environment.
"""

import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


def main():
    args = getResolvedOptions(
        sys.argv,
        ["JOB_NAME", "SOURCE_DATABASE", "SOURCE_TABLE", "TARGET_PATH"],
    )

    spark_context = SparkContext.getOrCreate()
    glue_context = GlueContext(spark_context)
    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)

    # Keep transformation_ctx stable between runs. Glue uses it to associate
    # bookmark state with this source.
    orders_dyf = glue_context.create_dynamic_frame.from_catalog(
        database=args["SOURCE_DATABASE"],
        table_name=args["SOURCE_TABLE"],
        transformation_ctx="orders_source",
    )

    # Write curated Parquet data partitioned by business date.
    # Use a controlled target prefix and define a retry/reconciliation strategy
    # appropriate to the table's business key and late-arriving data policy.
    glue_context.write_dynamic_frame.from_options(
        frame=orders_dyf,
        connection_type="s3",
        connection_options={
            "path": args["TARGET_PATH"],
            "partitionKeys": ["order_date"],
        },
        format="glueparquet",
        format_options={"compression": "snappy"},
        transformation_ctx="orders_target",
    )

    # Persist bookmark state only after the load steps complete successfully.
    job.commit()


if __name__ == "__main__":
    main()


# Operational checklist:
# 1. Grant the Glue role read access to the source/catalog and write access to target S3.
# 2. Enable job bookmarks and avoid changing transformation_ctx between deployments.
# 3. Validate source schema and the order_date partition format before production use.
# 4. Reconcile source/target counts and define handling for late-arriving records.
# 5. Make the target write retry-safe; bookmarks track source progress but do not
#    guarantee exactly-once delivery to a partially written target.
# 6. Use a controlled bookmark reset procedure when a deliberate backfill is needed.
