import fastai
from fastai  import *
from fastai.vision import *
import sys
import os

warnings.filterwarnings("ignore")

def Determine(path):
    path=os.path.dirname(os.path.abspath(__file__))
    learn=load_learner(r'{}'.format(path))
    img=open_image(path)
    k=learn.predict(img)[1]
    if k==1:
        return (0,'No Mask')
    else:
        return (1,'Mask')
    
    


