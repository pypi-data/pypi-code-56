import segmentation_models_pytorch as smp

from .fpn import get_fpn


class ModelLoader(object):

    def __init__(
            self,
    ):
        self.model = None
        self.loss = None

    def get_loss(self, loss_name):
        if loss_name == "DiceLoss":
            self.loss = smp.utils.losses.DiceLoss()
        return self.loss

    def get_model(
            self,
            model_name="FPN",
            encoder_name="se_resnext50_32x4d",
            encoder_weights="image_net",
            activation="sigmoid"
    ):

        if model_name == "FPN":
            self.model = get_fpn(encoder_name, encoder_weights, activation)
        else:
            #TODO: more models
            self.model = None
        return self.model
