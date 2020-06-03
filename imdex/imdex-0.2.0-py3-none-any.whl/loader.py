import os, pathlib
from google_drive_downloader import GoogleDriveDownloader as gdd
from tensorflow import data, image, io

current_path = str(pathlib.Path(__file__).parent.absolute())

files = [
    {
        "file_id":"1ImMtlGyk9IOghvfUxOP95iGSQ5irZi_7",
        "file_name":"tokenizer_1.pickle",
        "file_location":current_path + "/data/tokens/tokenizer_1.pickle"
    },
    {
        "file_id":"1BC4-QBpTsWKiiiP4UMBOeK0VYurORlTt",
        "file_name":"checkpoint",
        "file_location": current_path + "/data/ckp/checkpoint"
    },
    {
        "file_id":"1z9EGF2tNr_-dsvoEki0fykB8PJ9pLcYH",
        "file_name":"ckpt-7.data-00001-of-00002",
        "file_location": current_path + "/data/ckp/ckpt-7.data-00001-of-00002"
    },
    {
        "file_id":"1_oc_XoYPYqVIjHqBSkLFPlRn1sNoryDt",
        "file_name":"ckpt-7.index",
        "file_location":current_path + "/data/ckp/ckpt-7.index"
    },
    {
        "file_id":"1g2nrRRs6lFn7oF277tbTZkqf421plyD6",
        "file_name":"ckpt-7.data-00000-of-00002",
        "file_location": current_path + "/data/ckp/ckpt-7.data-00000-of-00002"
    },
    {
        "file_id":"1X4PRb-pDO6EG64pvYcPNwa-XbL6b4ZL7",
        "file_name":"glove_6B_50d_txt.word2vec",
        "file_location": current_path + "/data/word_embeddings/glove_6B_50d_txt.word2vec"
    }
]

def load_image(image_path, img_width=299, img_height=299):
    img = io.read_file(image_path)
    img = image.decode_jpeg(img, channels=3)
    img = image.resize(img, (img_width, img_height))
    return img

def __process_img(file_path):
    reference = file_path
    img = load_image(file_path)
    return img, reference

def load_foder(folder_path):
    images = []
    references = []
    list_ds = data.Dataset.list_files(folder_path+"/*")
    labeled_ds = list_ds.map(__process_img, num_parallel_calls=data.experimental.AUTOTUNE)
    for image, reference in labeled_ds:
        images.append(image.numpy())
        references.append(reference.numpy())

    return images, references

def is_files_downloaded():
    for file in files:
        path = file["file_location"].replace(r'\\',r'\/')
        if(not os.path.exists(path)):
            return False

    return True

def download_files():
    for file in files:
        path = file["file_location"].replace(r'\\',r'\/')
        gdd.download_file_from_google_drive(file_id=file["file_id"],
                                            dest_path=path,
                                            unzip=True)