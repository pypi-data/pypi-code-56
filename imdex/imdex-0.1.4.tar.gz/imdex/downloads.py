import os, pathlib
from google_drive_downloader import GoogleDriveDownloader as gdd

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

def is_files_downloaded():
    for file in files:
        path = file["file_location"].replace('\\','\/')
        if(not os.path.exists(path)):
            return False

    return True

def download_files():
    for file in files:
        path = file["file_location"].replace('\\','\/')
        gdd.download_file_from_google_drive(file_id=file["file_id"],
                                            dest_path=path,
                                            unzip=True)