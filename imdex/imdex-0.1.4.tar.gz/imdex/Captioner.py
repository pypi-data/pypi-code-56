from tensorflow import keras, expand_dims, nn, reduce_sum, concat, reshape, zeros, train, io, image, random
from imdex.downloads import download_files, is_files_downloaded

import numpy as np
import pickle
import pathlib

BATCH_SIZE = 64
embedding_dim = 256
units = 512
vocab_size = 5001
max_length = 49


class BahdanauAttention(keras.Model):
  
	def __init__(self, units):
		super(BahdanauAttention, self).__init__()
		self.W1 = keras.layers.Dense(units)
		self.W2 = keras.layers.Dense(units)
		self.V = keras.layers.Dense(1)

	def call(self, features, hidden):
		hidden_with_time_axis = expand_dims(hidden, 1)

		score = nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis))

		attention_weights = nn.softmax(self.V(score), axis=1)

		context_vector = attention_weights * features
		context_vector = reduce_sum(context_vector, axis=1)

		return context_vector, attention_weights

class CNN_Encoder(keras.Model):
    def __init__(self, embedding_dim):
        super(CNN_Encoder, self).__init__()
        self.fc = keras.layers.Dense(embedding_dim)

    def call(self, x):
        x = self.fc(x)
        x = nn.relu(x)
        return x

class RNN_Decoder(keras.Model):

	def __init__(self, embedding_dim, units, vocab_size):
		super(RNN_Decoder, self).__init__()
		self.units = units

		self.embedding = keras.layers.Embedding(vocab_size, embedding_dim)
		self.gru = keras.layers.GRU(self.units,
									return_sequences=True,
									return_state=True,
									recurrent_initializer='glorot_uniform')
		self.fc1 = keras.layers.Dense(self.units)
		self.fc2 = keras.layers.Dense(vocab_size)

		self.attention = BahdanauAttention(self.units)
  
	def call(self, x, features, hidden):
		
		context_vector, attention_weights = self.attention(features, hidden)

		x = self.embedding(x)

		x = concat([expand_dims(context_vector, 1), x], axis=-1)

		output, state = self.gru(x)

		x = self.fc1(output)

		x = reshape(x, (-1, x.shape[2]))

		x = self.fc2(x)

		return x, state, attention_weights

	def reset_state(self, batch_size):

		return zeros((batch_size, self.units))

class Captioner:

    def __init__(self):

        if(not is_files_downloaded()):
            download_files()

        current_path = str(pathlib.Path(__file__).parent.absolute()).replace('\\','\/')

        checkpoint_path = current_path + "/data/ckp"
        tokenizer_path = current_path + "/data/tokens/tokenizer_1.pickle"

        optimizer = keras.optimizers.Adam()

        self.encoder = CNN_Encoder(embedding_dim)
        self.decoder = RNN_Decoder(embedding_dim, units, vocab_size)

        self.ckpt = train.Checkpoint(encoder=self.encoder,
                                decoder=self.decoder,
                                optimizer = optimizer)
        
        self.ckpt_manager = train.CheckpointManager(self.ckpt, checkpoint_path, max_to_keep=5)    

        with open(tokenizer_path, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

        if self.ckpt_manager.latest_checkpoint:
            self.start_epoch = int(self.ckpt_manager.latest_checkpoint.split('-')[-1])
            self.ckpt.restore(self.ckpt_manager.latest_checkpoint)

        image_model = keras.applications.InceptionV3(include_top=False,
                                                weights='imagenet')
        new_input = image_model.input
        hidden_layer = image_model.layers[-1].output

        self.image_features_extract_model = keras.Model(new_input, hidden_layer)

    def load_image(self, image_path):
        img = io.read_file(image_path)
        img = image.decode_jpeg(img, channels=3)
        img = image.resize(img, (299, 299))
        img = keras.applications.inception_v3.preprocess_input(img)
        return img

    def __captionize(self, image):

        hidden = self.decoder.reset_state(batch_size=1)

        temp_input = expand_dims(image, 0)
        img_tensor_val = self.image_features_extract_model(temp_input)
        img_tensor_val = reshape(img_tensor_val, (img_tensor_val.shape[0], -1, img_tensor_val.shape[3]))

        features = self.encoder(img_tensor_val)

        dec_input = expand_dims([self.tokenizer.word_index['<start>']], 0)
        result = []

        for _ in range(max_length):
            predictions, hidden, _ = self.decoder(dec_input, features, hidden)

            predicted_id = random.categorical(predictions, 1)[0][0].numpy()
            result.append(self.tokenizer.index_word[predicted_id])

            if self.tokenizer.index_word[predicted_id] == '<end>':
                return result

            dec_input = expand_dims([predicted_id], 0)

        return result

    def captionize(self, images):
        captions = []
        for img in images:
            captions.append(self.__captionize(img))

        return captions