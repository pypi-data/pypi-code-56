import os
from axerflow.pyfunc import scoring_server
from axerflow.pyfunc import load_model


app = scoring_server.init(load_model(os.environ[scoring_server._SERVER_MODEL_PATH]))
