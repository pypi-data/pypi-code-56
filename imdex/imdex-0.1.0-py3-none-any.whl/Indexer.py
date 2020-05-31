import pandas as pd

from imdex.Captioner import Captioner
from gensim.models import KeyedVectors

class Indexer:

    def __init__(self, captions_csv_path=None):
        if(captions_csv_path == None):
            self.original_captions = []
            self.image_references = []
        else:
            captions_csv = pd.read_csv(captions_csv_path)
            self.original_captions = list(captions_csv.original_captions.apply(lambda s: eval(s)))
            self.image_references = list(captions_csv.image_references)
            
        self.cap = Captioner()
        self.we_model = KeyedVectors.load_word2vec_format("./imdex/data/word_embeddings/glove_6B_50d_txt.word2vec", binary=False)

    def add_images(self, images, references, redundancy=3):
        preds = self.cap.captionize(images)
        for index, sentence in enumerate(preds):
            self.original_captions.append(sentence)
            self.image_references.append(references[index])

    def query(self, query_text):
        proximits = [self.we_model.wmdistance(query_text.lower().split(), caption) for caption in self.original_captions]
        return sorted(zip(proximits, self.image_references))

    def save_to_csv(self, file_name):
        data_as_csv = pd.DataFrame({"original_captions":self.original_captions,
                                    "image_references":self.image_references})
        
        data_as_csv.to_csv(file_name, index=False)
        
    def load_image(self, image_path):
        return self.cap.load_image(image_path)