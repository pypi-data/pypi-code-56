import os

VOSPACE_BASE_DIRECTORY = 'vos:NewHorizons/S20A-OT04/SC_CORR/'
VOSPACE_MODEL_DIRECTORY = 'vos:jkavelaars/cadc_id_checker/'
SEX_EXECUTABLE = '/usr/local/bin/sex'

__PATH__ = os.path.dirname(__file__)
CONFIG = os.path.join(__PATH__, 'config')
os.environ['SEX_CONFIG'] = CONFIG
DEFAULT_SEX = os.path.join(CONFIG, 'default.sex')

DEEP_MODEL = os.path.join(CONFIG, 'Deep_model.h5')
SOM_MODEL = os.path.join(CONFIG, 'SOM_15x15.npy')
SOM_LABELS = os.path.join(CONFIG, 'Label_SOM_15x15.npy')
