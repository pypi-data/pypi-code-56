from utils import create_data_lists
from definitions import ROOT_DIR

if __name__ == '__main__':
    create_data_lists(voc07_path=ROOT_DIR/'data/VOC2007',
                      voc12_path=ROOT_DIR/'data/VOC2012',
                      output_folder=ROOT_DIR/'output')
