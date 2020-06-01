#!/usr/bin/env python
""" fcn

Last update: 1/5/20
"""

import segmentation_models_pytorch as smp


def get_fpn(
        encoder_name="se_resnext50_32x4d",
        encoder_weights="image_net",
        activation="sigmoid"
    ):
    model = smp.FPN(
        encoder_name=encoder_name,
        encoder_weights=encoder_weights,
        classes=1,
        decoder_dropout=0.05,
        activation=activation
    )
    return model
