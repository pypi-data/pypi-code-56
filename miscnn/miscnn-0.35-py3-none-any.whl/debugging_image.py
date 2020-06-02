# We are going to segment the celltracking dataset: PhC-C2DH-U373
# Source:   ISBI Cell Tracking Challenge 2015
#           http://celltrackingchallenge.net/2d-datasets/
#
# First we are going to setup our filestructure in order to use the Image IO Interface
# What we want for the Image_interface is something like that:
# # data/
# #      imgname001/imaging.png
# #                 segmentation.png
# #      imgname002/imaging.png
# #                 segmentation.png
# #      imgname003/imaging.png
# #                 segmentation.png
# #      ...

# Import some libraries
import os
import shutil
from PIL import Image
import numpy as np

# Configure data path for celltracking data set PhC-C2DH-U373 and file structure
path_dataset = "/home/mudomini/projects/celltracking.MIScnn/PhC-C2DH-U373/"
path_filestructure = "/home/mudomini/projects/celltracking.MIScnn/data"

# Initialize file structure
if not os.path.exists(path_filestructure): os.mkdir(path_filestructure)

# Iterate over both data sets
for ds in ["01", "02"]:
    # Define image directories
    path_ds_img = os.path.join(path_dataset, ds)
    path_ds_seg = os.path.join(path_dataset, ds + "_GT", "SEG")
    # Obtain sample list
    sample_list = os.listdir(path_ds_seg)
    # Remove every file which does not match image typ and preprocess sample names
    for i in reversed(range(0, len(sample_list))):
        if not sample_list[i].endswith(".tif"):
            del sample_list[i]
        else:
            sample_list[i] = sample_list[i][7:]
    # Iterate over each sample and transform the data into desired file structure
    for sample in sample_list:
        index = ds + "_" + sample[:-4]
        # Create sample directory
        path_sampleDir = os.path.join(path_filestructure, index)
        if not os.path.exists(path_sampleDir): os.mkdir(path_sampleDir)
        # Copy image file into filestructure
        path_ds_sample_img = os.path.join(path_ds_img, "t" + sample)
        path_fs_sample_img = os.path.join(path_sampleDir, "imaging.tif")
        shutil.copy(path_ds_sample_img, path_fs_sample_img)
        # Copy segmentation file into filestructure
        seg_file = "man_seg" + sample
        path_ds_sample_seg = os.path.join(path_ds_seg, seg_file)
        path_fs_sample_seg = os.path.join(path_sampleDir, "segmentation.tif")
        # Load segmentation from file
        seg_raw = Image.open(path_ds_sample_seg)
        # Convert segmentation from Pillow image to numpy matrix
        seg_pil = seg_raw.convert("LA")
        seg = np.array(seg_pil)
        # Keep only intensity and remove maximum intensitiy range
        seg_data = seg[:,:,0]
        # Union all separate cell classes to a single one
        seg_data[seg_data > 0] = 1
        # Transform numpy array back to a Pillow image & save to disk
        seg = Image.fromarray(seg_data)
        seg.save(path_fs_sample_seg, format="TIFF")

################################################################################
# Now, we can start setup our MIScnn pipeline

# Import some libraries
from miscnn import Data_IO, Preprocessor, Neural_Network
from miscnn.data_loading.interfaces import Image_interface
from miscnn.neural_network.metrics import tversky_crossentropy, dice_soft, \
                                          dice_crossentropy, tversky_loss
from miscnn.processing.subfunctions import Resize

# Initialize Data IO & Image Interface
interface = Image_interface(classes=2, img_type="grayscale", img_format="tif")
data_path = "/home/mudomini/projects/celltracking.MIScnn/data/"
data_io = Data_IO(interface, data_path, delete_batchDir=True)

# Obtain the sample list
sample_list = data_io.get_indiceslist()
sample_list.sort()
print(sample_list)

# for i in sample_list:
#     sample_test = data_io.sample_loader(i, load_seg=False)
#     print(sample_test.img_data.shape)

# # Run a test by pulling a sample and try to visualize it
# sample_test = data_io.sample_loader(sample_list[1], load_seg=True)
#
# img_data = sample_test.img_data
# print(img_data.shape[:-1])
# img = Image.fromarray(np.reshape(img_data, img_data.shape[:-1]))
# img.show()
#
# img_data = sample_test.seg_data * 100
# print(img_data.shape[:-1])
# img = Image.fromarray(np.reshape(img_data, img_data.shape[:-1]))
# img.show()

# # Create a clipping Subfunction to the lung window of CTs (-1250 and 250)
# sf_clipping = Clipping(min=-1250, max=250)
# # Create a pixel value normalization Subfunction to scale between 0-255
# sf_normalize = Normalization(mode="grayscale")
# # Create a pixel value normalization Subfunction for z-score scaling
# sf_zscore = Normalization(mode="z-score")
# Create a resizing Subfunction to shape 592x592
sf_resize = Resize((592, 592))

# Assemble Subfunction classes into a list
sf = [sf_resize]

# Initialize Preprocessor
pp = Preprocessor(data_io, data_aug=None, batch_size=1, subfunctions=sf,
                  prepare_subfunctions=True, prepare_batches=False,
                  analysis="fullimage")

 # Create the Neural Network model
model = Neural_Network(preprocessor=pp, loss=tversky_crossentropy,
                       metrics=[tversky_loss, dice_soft, dice_crossentropy],
                       batch_queue_size=3, workers=3, learninig_rate=0.001)

# # Define Callbacks
# cb_lr = ReduceLROnPlateau(monitor='loss', factor=0.1, patience=15,
#                          verbose=1, mode='min', min_delta=0.0001, cooldown=1,
#                          min_lr=0.00001)
# cb_es = EarlyStopping(monitor="loss", patience=100)
# cb_tb = TensorBoard(log_dir=os.path.join(fold_subdir, "tensorboard"),
#                    histogram_freq=0, write_graph=True, write_images=True)
# cb_cl = CSVLogger(os.path.join(fold_subdir, "logs.csv"), separator=',',
#                  append=True)

model.train(sample_list[5:], epochs=20, iterations=None)

model.predict(sample_list[0:5])
