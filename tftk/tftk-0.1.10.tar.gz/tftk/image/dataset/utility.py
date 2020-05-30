import tensorflow as tf
from typing import Dict,List, Callable



max_crop_width = 100
max_crop_height = 100

def resize_and_max_square_crop(data:Dict)->Dict:
    global max_crop_height
    global max_crop_width

    image = data['image']
    h = tf.shape(image)[0]
    w = tf.shape(image)[1]
    if ( h > w ):
         image = tf.image.crop_to_bounding_box(image,2//w,0,w,w)
    else:
        image = tf.image.crop_to_bounding_box(image,0,2//h,h,h)
    image = tf.image.resize(image,(max_crop_height,max_crop_width))
    data['image']  = tf.cast(image, tf.uint8)
    return data



class ImageDatasetUtil():

    def __init__(self):
        pass
    

    @classmethod
    def devide_train_validation(cls, dataset:tf.data.Dataset, length:int, ratio:float)->((tf.data.Dataset,int),(tf.data.Dataset,int)):
        """学習用と検証用のデータセットに分割する。
        
        Arguments:
            dataset -- 分割するデータセット
            length -- データセットの長さ
            ratio -- 学習用データセットの割合
        
        Returns:
            (Dataset,int),(Dataset,int) -- (学習用のデータセット、データセットのサイズ),(検証用データセット,データセットのサイズ)
        """

        train_size = int(length * ratio)
        validation_size = length - train_size
        train_set = dataset.take(train_size).skip(validation_size)
        validation_set = dataset.skip(train_size).take(validation_size)
        return ((train_set,train_size),(validation_set,validation_size))


    @classmethod
    def k_fold_cross_validation_dataset(cls, dataset:tf.data.Dataset, length:int, ratio:float)->((tf.data.Dataset,int),(tf.data.Dataset,int)):
        pass        

    @classmethod
    def count_image_dataset(cls, dataset:tf.data.Dataset)->(int, Dict):
        """データセットのラベルごとの数を数える。
        
        Arguments:
            cls {[type]} -- [description]
            Dict {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        total = 0
        count = {}
        for d in dataset:
            y = d["label"].numpy()
            c = count.get(y,0) + 1
            count[y] = c
            total = total + 1
        print(total)
        print(count)
        return total, count
    
    @classmethod
    def one_hot(cls, classes:int):
        """データセットに指定クラス数のone-hot処理を与えるmap関数

        
        Arguments:
            classes {int} -- [description]
        
        Returns:
            [type] -- [description]
        """
        def one_hot_map(data):
            data["label"] = tf.one_hot(data["label"], classes)
            return data
        return one_hot_map

    @classmethod
    def image_reguralization(cls, offset:float=0.0):
        """画像データを正則化するmap関数を作成する。
        
        Keyword Arguments:
            offset {float} -- [description] (default: {0.0})
        
        Returns:
            [type] -- [description]
        """
        def image_reguralization_map(data):
            data["image"]=tf.cast(data["image"], tf.float32)
            data["image"]=data["image"]/255.0 - offset
            return data
        return image_reguralization_map
    
    @classmethod
    def dataset_init_classification(cls, classes, offset:float=0.0)->Callable[[Dict],Dict]:
        """ 画像を数値/255.0、ラベルのont-hot化、オフセットの除去
        
        Arguments:
            classes {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        def __dataset_init_classification(data:Dict)->Dict:
            data["label"] = tf.one_hot(data["label"], classes)
            data["image"] = tf.cast(data["image"], tf.float32)
            data["image"] = (data["image"]/255.0) - offset
            return data
        return __dataset_init_classification
    
    @classmethod
    def dict_to_classification_tuple(cls):
        """dict形式のデータをtf.keras.Model.fit()用に変換する
        
        Returns:
            [type]: [description]
        """
        def __dict_to_classification_tuple(data:Dict)->(tf.Tensor,tf.Tensor):
            return (data["image"], data["label"])
        return __dict_to_classification_tuple
    

    @classmethod
    def dict_to_autoencoder_tuple(cls):
        """dict形式のデータをtf.keras.Model.fit()用に変換する
        
        Returns:
            [type]: [description]
        """
        def dict_to_ae_tuple(data:Dict)->(tf.Tensor,tf.Tensor):
            return (data["image"], data["image"])
        return dict_to_ae_tuple


    @classmethod
    def map_resize_with_crop_or_pad(cls, height:int, width:int)->Callable[[Dict],Dict]:
        """データセットの画像をクロップないしはパッドしてリサイズする。
        
        Args:
            h (int): リサイズする画像の高さ
            w (int): リサイズ後の画像の幅
        
        Returns:
            Mapする関数: Dataset.map()に適用する関数
        """
        global max_crop_height
        global max_crop_width

        max_crop_height = height
        max_crop_width = width

        return resize_and_max_square_crop


    @classmethod
    def map_max_square_crop_and_resize(cls,height:int, width:int)->Callable[[Dict],Dict]:
        global max_crop_height
        global max_crop_width

        max_crop_height = height
        max_crop_width = width
        return resize_and_max_square_crop

    @classmethod
    def resize(cls, h:int, w:int)->Callable[[Dict],Dict]:
        """データセットの画像をリサイズする。
        
        Args:
            h (int): リサイズする画像の高さ
            w (int): リサイズ後の画像の幅
        
        Returns:
            Mapする関数: Dataset.map()に適用する関数
        """

        def __resize(data:Dict)->Dict:
            data["image"] = tf.image.resize(data["image"], (h,w))
            return data
        return __resize