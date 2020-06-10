from torch import nn

_activation_map = {
    "relu": nn.ReLU(),
    "lrelu": nn.LeakyReLU(),
    "sigmoid": nn.Sigmoid(),
    "tanh": nn.Tanh(),
    "elu": nn.ELU(),
    "selu": nn.SELU(),
    "lsoftmax": nn.LogSoftmax(1),
    "none": nn.Identity()
}

_activation = [nn.ReLU, nn.LeakyReLU, nn.Sigmoid, nn.Tanh, nn.ELU, nn.SELU, nn.LogSoftmax, nn.Identity]


class LinearBlock(nn.Module):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, none}
    """
    def __init__(self, n_input, n_output, activation="relu", batchnorm=False, dropout=0):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("lin", nn.Linear(n_input, n_output))

        if batchnorm:
            self.block.add_module("bn", nn.BatchNorm1d(n_output))

        if activation in _activation_map:
            self.block.add_module(activation, _activation_map[activation])
        elif type(activation) in _activation:
            self.block.add_module("activation", activation)
        else:
            raise Exception(f"jcopdl supports these activations ({', '.join(_activation_map.keys())})")

        if dropout > 0:
            self.block.add_module("do", nn.Dropout(dropout))

    def forward(self, x):
        return self.block(x)


class ConvBlock(nn.Module):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, none}
    available pool_type {maxpool, avgpool}
    """
    def __init__(self, in_channel, out_channel, kernel=3, stride=1, pad=1, activation="relu",
                 batchnorm=False, dropout=0, pool=None, pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("conv2d", nn.Conv2d(in_channel, out_channel, kernel, stride, pad))

        if batchnorm:
            self.block.add_module("bn2d", nn.BatchNorm2d(out_channel))

        if activation in _activation_map:
            self.block.add_module(activation, _activation_map[activation])
        elif type(activation) in _activation:
            self.block.add_module("activation", activation)
        else:
            raise Exception(f"jcopdl supports these activations ({', '.join(_activation_map.keys())})")

        if dropout > 0:
            self.block.add_module("do2d", nn.Dropout2d(dropout))

        if pool == "maxpool":
            self.block.add_module("maxpool", nn.MaxPool2d(pool_kernel, pool_stride))
        elif pool == "avgpool":
            self.block.add_module("avgpool", nn.AvgPool2d(pool_kernel, pool_stride))
        elif pool is not None:
            raise Exception("jcopdl supports these pooling ({maxpool, avgpool})")

    def forward(self, x):
        return self.block(x)


class TConvBlock(nn.Module):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, none}
    available pool_type {maxpool, avgpool}
    """
    def __init__(self, in_channel, out_channel, kernel=3, stride=1, pad=1, activation="relu",
                 batchnorm=False, dropout=0, pool=None, pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("tconv2d", nn.ConvTranspose2d(in_channel, out_channel, kernel, stride, pad))

        if batchnorm:
            self.block.add_module("bn2d", nn.BatchNorm2d(out_channel))

        if activation in _activation_map:
            self.block.add_module(activation, _activation_map[activation])
        elif type(activation) in _activation:
            self.block.add_module("activation", activation)
        else:
            raise Exception(f"jcopdl supports these activations ({', '.join(_activation_map.keys())})")

        if dropout > 0:
            self.block.add_module("do2d", nn.Dropout2d(dropout))

        if pool == "maxpool":
            self.block.add_module("maxpool", nn.MaxPool2d(pool_kernel, pool_stride))
        elif pool == "avgpool":
            self.block.add_module("avgpool", nn.AvgPool2d(pool_kernel, pool_stride))
        elif pool is not None:
            raise Exception("jcopdl supports these pooling ({maxpool, avgpool})")

    def forward(self, x):
        return self.block(x)


class VGGBlock(nn.Module):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, none}
    """
    def __init__(self, in_channel, out_channel, n_repeat=2, kernel=3, stride=1, pad=1, activation="relu",
                 batchnorm=False, dropout=0, pool="maxpool", pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("conv_block0",
                              ConvBlock(in_channel, out_channel, kernel, stride, pad, activation, batchnorm, dropout))

        for i in range(1, n_repeat):
            if i == (n_repeat - 1):
                self.block.add_module(f"conv_block{i}",
                                      ConvBlock(out_channel, out_channel, kernel, stride, pad, activation, batchnorm,
                                                dropout, pool, pool_kernel, pool_stride))
            else:
                self.block.add_module(f"conv_block{i}",
                                      ConvBlock(out_channel, out_channel, kernel, stride, pad, activation, batchnorm,
                                                dropout))

    def forward(self, x):
        return self.block(x)
