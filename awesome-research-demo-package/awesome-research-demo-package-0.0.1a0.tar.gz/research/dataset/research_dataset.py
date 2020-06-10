
import numpy as np
    
from sapsan.core.abstrctions.dataset import Dataset
    
    
class ResearchDataset(Dataset):
    def load(self):
        return np.random.random((4, 4))

