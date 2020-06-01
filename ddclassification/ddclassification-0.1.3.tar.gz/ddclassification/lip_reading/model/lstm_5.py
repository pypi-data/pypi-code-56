import tensorflow as tf
from tensorflow.keras import layers


class Lstm_5(tf.keras.Model):

    def __init__(self):
        super(Lstm_5, self).__init__()
        self.td_conv1 = layers.TimeDistributed(layers.Conv2D(96, (3, 3), strides=1))
        self.td_maxPool1 = layers.TimeDistributed(layers.MaxPooling2D((3, 3), strides=2))

        self.td_conv2 = layers.TimeDistributed(layers.Conv2D(256, (3, 3), strides=2))
        self.td_maxPool2 = layers.TimeDistributed(layers.MaxPooling2D((3, 3), strides=2))

        self.td_conv3 = layers.TimeDistributed(layers.Conv2D(512, (3, 3), strides=1))

        self.td_conv4 = layers.TimeDistributed(layers.Conv2D(512, (3, 3), strides=1))

        self.td_conv5 = layers.TimeDistributed(layers.Conv2D(512, (3, 3), strides=1))
        self.td_maxPool5 = layers.TimeDistributed(layers.MaxPooling2D((3, 3), strides=2))

        self.td_fc6 = layers.TimeDistributed(layers.Dense(4096))
        self.td_flat6 = layers.TimeDistributed(layers.Flatten())

        self.lstm7 = layers.LSTM(512, return_sequences=True)
        self.lstm8 = layers.LSTM(512)

        self.fc9 = layers.Dense(26)
        self.softmax9 = layers.Activation('softmax')

    def call(self, inputs):
        x = self.td_conv1(inputs)
        x = self.td_maxPool1(x)

        x = self.td_conv2(x)
        x = self.td_maxPool2(x)

        x = self.td_conv3(x)

        x = self.td_conv4(x)

        x = self.td_conv5(x)
        x = self.td_maxPool5(x)

        x = self.td_fc6(x)
        x = self.td_flat6(x)

        x = self.lstm7(x)
        x = self.lstm8(x)

        x = self.fc9(x)
        return self.softmax9(x)
