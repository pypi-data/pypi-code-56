from axerflow.pyfunc import scoring_server
from axerflow import pyfunc
app = scoring_server.init(pyfunc.load_pyfunc("/opt/ml/model/"))
