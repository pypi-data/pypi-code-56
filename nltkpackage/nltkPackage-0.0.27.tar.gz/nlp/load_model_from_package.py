import mlflow
import mlflow.spark
import mlflow.pyfunc


def read_pyspark_model(path):
    # newv = "nltkTransformer-0.0.12/nlp/"
    # return mlflow.spark.load_model(site.getsitepackages()[0] + "/nlp/")
    return mlflow.spark.load_model(".")
