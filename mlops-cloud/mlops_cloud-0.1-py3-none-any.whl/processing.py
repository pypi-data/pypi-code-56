import sys
import os
import boto3
import pandas as pd
import io
import time
import random

sys.path.append(f"{os.getcwd()}/mlops")
from awsglue.utils import getResolvedOptions

AWS_REGION = os.environ["AWS_REGION"]
FINISHED_STATUS = ["SUCCEEDED", "FAILED", "CANCELLED"]
OUTPUT_PATH = "athena_queries/output"


class Processor:
    def __init__(self):
        args = getResolvedOptions(
            sys.argv,
            ["JOB_NAME", "output_path", "splits", "subsets", "databases", "tables"],
        )
        self.output_path = args["output_path"]
        self.job_name = args["JOB_NAME"]
        self.bucket = args["bucket"]
        self.splits = [float(x) for x in args["splits"].split(",")]
        self.subsets = [float(x) for x in args["subsets"].split(",")]
        self.databases = [str(x) for x in args["databases"].split(",")]
        self.tables = [str(x) for x in args["tables"].split(",")]


class PythonProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.athena = boto3.client("athena", region_name=AWS_REGION)
        self.s3 = boto3.resource("s3", region_name=AWS_REGION)

    def _generate_subset(self, data: pd.DataFrame, fraction: float):
        return data.sample(
            frac=fraction, random_state=random.randint(1, 10000)
        ).reset_index(drop=True)

    def _split_data(self, data):
        if len(self.splits) == 1:
            return {"train": data}
        if len(self.splits) == 2:
            train = data.sample(
                frac=self.splits[0], random_state=random.randint(1, 10000)
            )
            val = data.drop(train.index)
            return {"train": train, "val": val}
        if len(self.splits) == 3:
            train_val = data.sample(
                frac=self.splits[0] + self.splits[1],
                random_state=random.randint(1, 10000),
            )
            test = data.drop(train.index)
            train = train_val.sample(
                frac=self.splits[0], random_state=random.randint(1, 10000)
            )
            val = train_val.drop(train.index)
            return {"train": train, "val": val, "test": test}

    def _save_csv(self, df: pd.DataFrame, split: str, subset: float):
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, header=False, index=False)
        self.s3.Bucket(self.bucket).put_object(
            Body=csv_buffer.getvalue(),
            Key=f"{self.output_path}/subset={int(subset*100)}/split={split}/{split}.csv",
        )

    def _save_to_s3(self, splits: dict, subset: float, output_format: str):
        if output_format == "csv":
            for k, v in self.splits.items():
                self._save_csv(df=v, split=k, subset=subset)
        else:
            raise (
                "Currently only CSV is supported as output format for Pandas and Scikit processing jobs."
            )

    def parse_result(self, qry_id: str):
        res = (
            self.s3.resource.Bucket(self.bucket)
            .Object(key=f"{OUTPUT_PATH}/{qry_id}.csv")
            .get()
        )
        return pd.read_csv(io.BytesIO(res["Body"].read()), encoding="utf8")

    def read(self, database: str, table: str, qry=None):
        if qry is None:
            qry = f"SELECT * FROM {database}.{table}"
        response_query_execution_id = self.athena.start_query_execution(
            QueryString=qry,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": f"s3://{self.bucket}/{OUTPUT_PATH}"},
        )

        response_get_query_details = self.athena.get_query_execution(
            QueryExecutionId=response_query_execution_id["QueryExecutionId"]
        )
        status = "QUEUED"

        while status not in FINISHED_STATUS:
            response_get_query_details = self.athena.get_query_execution(
                QueryExecutionId=response_query_execution_id["QueryExecutionId"]
            )
            status = response_get_query_details["QueryExecution"]["Status"]["State"]
            if status == "FAILED" or status == "CANCELLED":
                return False, False
            elif status == "SUCCEEDED":
                return self.parse_result(
                    response_query_execution_id["QueryExecutionId"]
                )
            else:
                time.sleep(1)

        return False

    def write(self, df: pd.DataFrame, output_format="csv"):
        for subset in self.subsets:
            df_subset = self._generate_subset(df, subset)
            df_splits = self._split_data(df_subset)
            self._save_to_s3(df_splits, subset, output_format)

    def clean_up(self):
        bucket = self.s3.Bucket(self.bucket)
        for obj in bucket.objects.filter(Prefix=OUTPUT_PATH):
            self.s3.Object(bucket.name, obj.key).delete()


class SparkProcessor(Processor):
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame
    from awsglue.job import Job
    from pyspark.sql import SparkSession, DataFrame

    def __init__(self):
        super().__init__()
        self.spark = self.SparkSession.builder.appName("MLOps").getOrCreate()
        self.glue = self.GlueContext(self.spark)
        self.job = self.Job(self.glue)
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

    def _save_to_s3(self, splits: dict, subset: float, output_format: str):
        for k, v in self.splits.items():
            dyf = self.DynamicFrame.fromDF(v, self.glue, f"resultDyf{k}")
            self.glue.write_dynamic_frame.from_options(
                frame=dyf,
                format=output_format,
                format_options={"writeHeader": False},
                connection_type="s3",
                connection_options={
                    "path": f"{self.output_path}/subset={int(subset*100)}/split={k}"
                },
            )

    def read(self, database_name: str, table_name: str):
        return self.glue.create_dynamic_frame.from_catalog(
            database=database_name,
            table_name=table_name,
            transformation_ctx=f"{self.job_name}_read",
        )

    def write(self, df: DataFrame, output_format="csv"):
        self.job.commit()
        for subset in self.subsets:
            df_subset = self._generate_subset(df, subset)
            df_splits = self._split_data(df_subset)
            self._save_to_s3(df_splits, subset, output_format)
