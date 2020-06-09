from abc import ABC, abstractmethod


# -----------------------------------------------------------------------------#

class BackboneInterface(ABC):

    @abstractmethod
    def get_backbone_builder(self):
        """
        Return a builder function and tensorflow argument scope.

        Return:
            builder: Function with signature:
                         features, end_points, pre_reduce_endpoints = fn(backbone, images, is_training, input_to_output_ratio=None, reuse=None)
                     with:
                        - backbone: A deepomatic.oef.models.image.backbones.Backbone instance.
                        - images: The preprocessed input tensor
                        - is_training: whether dropout should be active and batch_norm trainable
                        - input_to_output_ratio: if not None, `features` must be a feature map suited for detection or segmentation
                                                 The feature map size should be roughly the input size divided by input_to_output_ratio.
                        - reuse: re-use the weights of the backbone. Typically used in siamese networks.
                        - features: A tensor
                        - end_points: A dict of tensors indexed by strings (see aux_list below)
                        - pre_reduce_endpoints: A dict of tensor indexed by integers which reprensent the input-size-to-tensor-size ratio.
                                                Those are the lastest tensors with such ratios.
            aux_list: Auxiliary logits list. Each items of the list is function
                      with the following signature: logits_tensor = aux_fn(endpoints)
                      with `endpoints` as returned by the builder.
            scope_name: scope name of the backbone. Used by feature extractors to build feature pyramids.
        """
        pass
