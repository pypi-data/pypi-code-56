
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession, DataFrame
import random
import sys


class SparkProcessor():
    def __init__(self):
        args = getResolvedOptions(
            sys.argv,
            [
                "JOB_NAME",
                "type",
                "bucket",
                "output_path",
                "splits",
                "subsets",
                "databases",
                "tables",
            ],
        )
        self.output_path = args["output_path"]
        self.job_name = args["JOB_NAME"]
        self.bucket = args["bucket"]
        self.splits = [float(x) for x in args["splits"].split(",")]
        self.subsets = [float(x) for x in args["subsets"].split(",")]
        self.databases = [str(x) for x in args["databases"].split(",")]
        self.tables = [str(x) for x in args["tables"].split(",")]
        self.spark = SparkSession.builder.appName("MLOps").getOrCreate()
        self.glue = GlueContext(self.spark)
        self.job = Job(self.glue)
        self.job.init(self.job_name)

    def _generate_subset(self, data: DataFrame, fraction: float):
        return data.sample(fraction=fraction, seed=random.randint(1, 10000))

    def _split_data(self, data):
        if len(self.splits) == 1:
            return {"train": data}
        if len(self.splits) == 2:
            train, val = data.randomSplit(self.splits, seed=random.randint(1, 10000))
            return {"train": train, "val": val}
        if len(self.splits) == 3:
            train, val, test = data.randomSplit(
                self.splits, seed=random.randint(1, 10000)
            )
            return {"train": train, "val": val, "test": test}

    def _save_to_s3(self, data_splits: dict, subset: float, coalesce: int, partitions: list, output_format: str, header: bool):
        for k, v in data_splits.items():
            if coalesce:
                dyf = DynamicFrame.fromDF(v, self.glue, f"resultDyf{k}").coalesce(coalesce)
            else:
                dyf = DynamicFrame.fromDF(v, self.glue, f"resultDyf{k}")
            path = f"s3://{self.bucket}/{self.output_path}/subset={int(subset*100)}/split={k}"
            if output_format == "csv":
                format_options = {
                    "writeHeader": header
                }
            elif output_format == "parquet":
                format_options = {
                    "compression": "gzip"
                }
                output_format = "glueparquet"
            if partitions is None:
                connection_options = {
                    "path": path
                }
            else:
                connection_options = {
                    "path": path,
                    "partitionKeys": partitions
                }
            self.glue.write_dynamic_frame.from_options(
                frame=dyf,
                format=output_format,
                format_options=format_options,
                connection_type="s3",
                connection_options=connection_options
            )

    def read(self, database_name: str, table_name: str):
        return self.glue.create_dynamic_frame.from_catalog(
            database=database_name,
            table_name=table_name,
            transformation_ctx=f"{self.job_name}_read",
        )

    def write(self, df: DataFrame, coalesce=0, partitions: list=None, output_format="parquet", header=True):
        self.job.commit()
        for subset in self.subsets:
            df_subset = self._generate_subset(df, subset)
            df_splits = self._split_data(df_subset)
            self._save_to_s3(df_splits, subset, coalesce, partitions, output_format, header)