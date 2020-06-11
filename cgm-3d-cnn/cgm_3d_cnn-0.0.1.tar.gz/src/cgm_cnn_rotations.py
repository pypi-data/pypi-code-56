# course grained cnn on 38 proteins (small practice dataset)
from rotations import rotation_combo
from matplotlib import pyplot as plt
import numpy as np
import os
import sys
import random

try:
  import keras
  from keras.models import Sequential
  from keras.layers import Dense, Dropout, Activation, Flatten
  from keras.layers import Convolution3D
  from keras.optimizers import Adam
  from keras.callbacks import Callback
  from keras.models import load_model
  from keras.utils import multi_gpu_model
  from keras.utils import np_utils
  from keras.utils import to_categorical

except ImportError:
  import tensorflow
  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
  from tensorflow.keras.layers import Convolution3D
  from tensorflow.keras.callbacks import Callback
  from tensorflow.keras.optimizers import Adam
  from tensorflow.keras.models import load_model
  from tensorflow.keras.utils import multi_gpu_model
  from tensorflow.keras.utils import np_utils
  from tensorflow.keras.utils import to_categorical
  
# fill a box
def make_one_box(pre_box):
  box = np.zeros([9, 9, 9, 20]) # 4D array filled with 0

  for ind_set in pre_box:
    box[ind_set[0]][ind_set[1]][ind_set[2]][ind_set[3]] += 1

  return box

# returns list of condensed boxes
def get_box_list(path): 
  fileList = os.listdir(path)
  pre_box_list = []
  center_aa_list = []

  for file in fileList:
    if "boxes" in file:
      pdb_id = file[-8:-4]

      pre_boxes = np.load(path + file, allow_pickle = True)
      for pre_box in pre_boxes:
        pre_box_list.append(pre_box)

      centers = np.load(path + "centers_" + pdb_id + ".npy", allow_pickle = True) # list of center aa's in one file
      for center in centers:
        center_aa_list.append(center)
  
  return pre_box_list, center_aa_list

# generator for validation data
def test_val_dataGenerator(pre_boxes, center_aa_list, batch_size):
  while True:
      for i in range(0, len(pre_boxes) - batch_size, batch_size):
        box_list = []
        center_list = []
        for j in range(i, i + batch_size): 
          box = make_one_box(pre_boxes[j])
          box_list.append(box)
          center_list.append(center_aa_list[j])

        yield np.asarray(box_list), np_utils.to_categorical(center_list, 20)

# generator for training data
def train_dataGenerator(pre_boxes, center_aa_list, batch_size, rotations):
  zip_lists = list(zip(pre_boxes, center_aa_list))
  random.shuffle(zip_lists)
  pre_boxes, center_aa_list = list(zip(*zip_lists))

  while True:
      batch_fraction = int(batch_size/rotations)
      for i in range(0, len(pre_boxes) - batch_fraction, batch_fraction):
        box_list = []
        center_list = []
        for j in range(i, i + batch_fraction): 
          rotated_boxes = rotation_combo(pre_boxes[j], rotations)
          for rotated_box in rotated_boxes:
            box_list.append(make_one_box(rotated_box))
          for z in range(0, rotations):
            center_list.append(center_aa_list[j])

        yield np.asarray(box_list), np_utils.to_categorical(center_list, 20)

# preparing testing data
def get_test_data(path_x, path_y):
  x_data_test = np.load(path_x, allow_pickle = True)
  y_data_test = np.load(path_y, allow_pickle = True)
  
  x_test = []
  for index_set  in x_data_test:
    box = make_one_box(index_set)
    x_test.append(box)

  x_test = np.asarray(x_test)
  y_test = np_utils.to_categorical(y_data_test, 20)

  return x_test, y_test

# cnn model structure
def create_model():
  model = Sequential()
  model.add(Convolution3D(32, kernel_size = (3, 3, 3), strides = (1, 1, 1), activation = 'relu', input_shape = (9, 9, 9, 20))) # 32 output nodes, kernel_size is your moving window, activation function, input shape = auto calculated
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Flatten()) # now our layers have been combined to one
  model.add(Dense(500, activation = 'relu')) # 500 nodes in the last hidden layer
  model.add(Dense(20, activation = 'softmax')) # output layer has 20 possible classes (amino acids 0 - 19)

  model = multi_gpu_model(model, gpus=4)

  model.compile(loss ='categorical_crossentropy', optimizer = Adam(lr = .001), metrics = ['accuracy'])

  return model

# training the model
def train_model(model, batch_size, epochs, rotations, x_train, y_train, x_val, y_val):

  history = model.fit_generator(
            generator = train_dataGenerator(x_train, y_train, batch_size, rotations),
            validation_data = test_val_dataGenerator(x_val, y_val, batch_size),
            validation_steps = 20,
            steps_per_epoch = len(x_train)/batch_size, 
            epochs = epochs, 
            verbose = 1,
          )

  return history

# returns testing results
def get_testing_results(model, batch_size, x_test, y_test):
  score = model.evaluate(x_test, y_test, verbose = 1, steps = int(len(x_test)/batch_size))  
  #score = model.evaluate_generator(x_test, y_test, verbose = 1, steps = int(len(x_test)/batch_size))
  model.save('model.h5')

  return score
  
#graphing the accuracy and loss for both the training and test data
def get_plots(history):
  #summarize history for accuracy 
  plt.plot(history.history['accuracy'])
  plt.plot(history.history['val_accuracy'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['training', 'validation'], loc = 'upper left')
  plt.savefig("Accuracy_cgm_flips.pdf")
  plt.clf()

  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['training', 'validaton'], loc = 'upper left')
  plt.savefig("Loss_cgm_flips.pdf")

#---------------------------main----------------------------------------------------
# variables
EPOCHS = 1 # iterations through the data
ROTATIONS = 4 # number of box rotations
BATCH_SIZE = 20 # batch_size must be divisible by "ROTATIONS"

# data paths
training_path = "./boxes/"
validation_path = "./boxes_38/"
testing_path_x = "./testing/boxes_test.npy"
testing_path_y = "./testing/centers_test.npy"

# training and validation
x_train, y_train = get_box_list(training_path) # preparing training data (boxes, centers)
x_val, y_val = get_box_list(validation_path) # preparing validation data (boxes, centers)
model = create_model()
history = train_model(model, BATCH_SIZE, EPOCHS, ROTATIONS, x_train, y_train, x_val, y_val)

# testing
x_test, y_test = get_test_data(testing_path_x, testing_path_y)
score = get_testing_results(model, BATCH_SIZE, x_test, y_test)

# results
get_plots(history)
print('Test loss:', score[0])
print('Test accuracy:', score[1])








