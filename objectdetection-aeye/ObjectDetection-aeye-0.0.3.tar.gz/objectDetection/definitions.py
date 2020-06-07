# This contains all the definitions that will be used in the program
from pathlib import Path

import torch

CWD = Path(__file__).parent
ROOT_DIR = CWD.parent

device = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')
cpu = torch.device('cpu')
