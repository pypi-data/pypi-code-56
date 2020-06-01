import os
import tensorflow as tf
import numpy as np

class DataGenerator(tf.keras.utils.Sequence):
    def __init__(self, data_path,solver,type='train', batch_size=32, shuffle=True, augment=True,output_shape=(26,111,111,5)):
        self.output_shape = output_shape
        self.solver = solver
        self.data_path = data_path
        self.path = os.path.join(self.data_path,type)
        self.n_classes = len(os.listdir(self.path))
        print(self.n_classes)

        self.classes = {}
        for i,classname in enumerate(os.listdir(self.path)):
            self.classes.update({classname:i})

        self.labels = {}
        self.list_IDs = []

        for classname in os.listdir(self.path):
            class_path = os.path.join(self.path,classname)
            for one_data in os.listdir(class_path):
                one_data_path = os.path.join(class_path,one_data)
                self.list_IDs.append(one_data_path)
                self.labels.update({one_data_path:self.classes[classname]})

        self.batch_size = batch_size
        self.shuffle = shuffle
        self.augment = augment
        print(self.labels)
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        x, y = self.__data_generation(list_IDs_temp)
        return x, y

    def __data_generation(self, list_IDs_temp):
        data = []

        y = np.empty((self.batch_size), dtype=int)

        for i, ID in enumerate(list_IDs_temp):
            data.append(self.solver(ID))
            y[i] = self.labels[ID]

        data = np.array(data)
        data = data.reshape(self.batch_size,*self.output_shape)

        return data, tf.keras.utils.to_categorical(y, num_classes=self.n_classes)

