import mlflow
import mlflow.spark
import mlflow.pyfunc
from os import listdir


def read_pyspark_model(path):
    # newv = "nltkTransformer-0.0.12/nlp/"
    # return mlflow.spark.load_model(site.getsitepackages()[0] + "/nlp/")
    print(listdir("."))
    return mlflow.spark.load_model(".")
