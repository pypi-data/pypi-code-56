import mlflow
import mlflow.spark
import mlflow.pyfunc
import site
# import nlp


def read_pyspark_model(path):
    # newv = "nltkTransformer-0.0.12/nlp/"
    # return mlflow.spark.load_model(site.getsitepackages()[0] + "/nlp/")
    return mlflow.spark.load_model(path)

def read_pyfunc_model():
    # newv = "nltkTransformer-0.0.12/nlp/"
    # return mlflow.pyfunc.load_model(site.getsitepackages()[0] + "/nlp/")
    return mlflow.pyfunc.load_model("/opt/anaconda3/envs/azurefunc/lib/python3.7/site-packages/nlp" + "")
#
# print(read_model())
# # from pyspark.sql import SparkSession
#
# # spark = SparkSession.builder.getOrCreate()
# mlflow.spark.load_model("/Users/ravi.teja/Work/nltkTransformer/nlp/")
# from platform import python_version
#
# print(python_version())
