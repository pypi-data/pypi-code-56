# -*- coding: utf-8 -*-
"""
Base predictor
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import logging
from dg_predictor import dg_dataformat


__all__ = ['BasePredictor', 'Engine']


class Engine(object):

    def __init__(self, config):
        """init func

        parameters
        ----------
        config : edict
            predictor config   

        """
        self.config = config
        # mxnet, pytorch
        self.data_batch = None
        # tensorflow
        self.fetch_dict = None
        self.feed_dict = None
        # ouytput
        self.network_outputs = None
        self._init_engine()

    def _init_engine(self):
        if 'mxnet-symbol' in self.config.engine:
            self._create_mxnet_symbol()
        elif 'mxnet-gluon' in self.config.engine:
            self._create_mxnet_gluon()
        elif 'tensorflow' in self.config.engine:
            self._create_tensorflow()
        elif 'pytorch' in self.config.engine:
            self._create_pytorch()
        else:
            raise NotImplementedError

    def forward(self):
        if 'mxnet-symbol' in self.config.engine:
            self._forward_mxnet_symbol()
        elif 'mxnet-gluon' in self.config.engine:
            self._forward_mxnet_gluon()
        elif 'tensorflow' in self.config.engine:
            self._forward_tensorflow()
        elif 'pytorch' in self.config.engine:
            self._forward_pytorch()
        else:
            raise NotImplementedError

    def _create_mxnet_symbol(self):
        import mxnet as mx
        if self.config.gpus == '-1':
            self.ctx = [mx.cpu()]
            logging.info("CPU MODE")
            if self.config.batch_size > 1:
                logging.error("Please set batch_size to 1")
                import sys; sys.exit()
        else:
            self.ctx = [mx.gpu(int(i)) for i in self.config.gpus.split(',')]
            logging.info("GPU MODE")
            assert self.config.batch_size >= len(self.ctx)
        symbol = mx.symbol.load(self.config.json)
        input_shape = [int(x) for x in self.config.input_shape.split(',')]

        data_names = ['data', ]
        module = mx.module.Module(symbol=symbol, data_names=tuple(data_names), label_names=None, context=self.ctx)
        data_shape = (self.config.batch_size, input_shape[2], input_shape[0], input_shape[1])
        module.bind(for_training=False, data_shapes=[('data', data_shape),], label_shapes=None)

        arg_params, aux_params = load_param(self.config.params)
        module.set_params(arg_params, aux_params, allow_missing=True, allow_extra=True)
        self.module = module

    def _create_mxnet_gluon(self):
        import mxnet as mx
        if self.config.gpus == '-1':
            self.ctx = [mx.cpu()]
        else:
            self.ctx = [mx.gpu(int(i)) for i in self.config.gpus.split(',')]
        self.net = mx.gluon.SymbolBlock.imports(self.config.json, ['data'])
        self.net.load_parameters(filename=self.config.params,
                                 ctx=self.ctx,
                                 allow_missing=True,
                                 ignore_extra=True)
        self.net.collect_params().reset_ctx(self.ctx)
        self.net.hybridize(static_alloc=True)

    def _create_tensorflow(self):
        import tensorflow as tf
        if self.config.gpus == '-1':
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] = self.config.gpus
        self.sess = tf.Session(graph=tf.Graph())
        tf.save_model.loader.load(self.sess, ["serve"], self.config.model_path)

    def _create_pytorch(self):
        import torch
        self.model = torch.load(self.config.model_path)
        self.model.eval()
        if self.config.gpus == '-1':
            self.device = torch.device('cpu')
            pass
        else:
            device_ids = [int(i) for i in self.config.gpus.split(',')]
            self.model = torch.nn.DataParallel(self.model, device_ids=device_ids)

    def _forward_mxnet_symbol(self):
        self.module.forward(self.data_batch)
        self.network_outputs = self.module.get_outputs()

    def _forward_mxnet_gluon(self):
        import mxnet as mx
        if isinstance(self.data_batch, mx.nd.NDArray):
            data_batch = mx.gluon.utils.split_and_load(self.data_batch, self.ctx, batch_axis=0, even_split=False)
            network_outputs = list()
            for each_gpu in data_batch:
                network_outputs.append(self.net(each_gpu).as_in_context(mx.cpu())) 
            self.network_outputs = mx.nd.concat(*network_outputs, dim=0)
        else:
            self.network_outputs = self.net(self.data_batch[0][0])
        if isinstance(self.network_outputs, mx.nd.NDArray):
            self.network_outputs = [self.network_outputs]

    def _forward_tensorflow(self):
        self.network_outputs = self.sess.run(self.fetch_dict, self.feed_dict)

    def _forward_pytorch(self):
        self.network_outputs = self.model(self.data_batch)


class BasePredictor(object):

    """base predictor"""

    def __init__(self, config, task_name):
        """init func

        parameters
        ----------
        config : edict
            predictor config   
        task_name : str
            task name

        """
        self.config = config
        self.task_name = task_name
        # mxnet, pytorch, tensorflow
        self.data_batch = None
        self.fetch_dict, feed_dict = None, None
        # ouytput
        self.network_outputs = None
        # source
        self.source = None

    def create_predictor(self):
        logging.info('Create %s ...' % self.task_name)
        self.engine = Engine(self.config)

    def create_source(self):
        """
        create data IO.

        """
        if self.source is not None:
            return 
        dgtxt = getattr(self.config, 'dgtxt', None)
        field = getattr(self.config, 'field', None)
        dgjson = getattr(self.config, 'dgjson', None)
        task = getattr(self.config, 'task', None)
        roidb = getattr(self.config, 'roidb', None)
        assert field is not None if dgtxt is not None else True
        assert task is not None if dgjson is not None else True
        if dgtxt is not None:
            inputfile = dgtxt
        elif dgjson is not None:
            inputfile = dgjson
        elif roidb is not None:
            inputfile = roidb
        else:
            inputfile = None
        imgdir = getattr(self.config, 'imgdir', None)
        imgrec = getattr(self.config, 'imgrec', None)
        videofile = getattr(self.config, 'videofile', None)
        self.source = dg_dataformat.Input(
                        inputfile=inputfile,
                        field=field,
                        task=task,
                        imgdir=imgdir,
                        imgrec=imgrec,
                        videofile=videofile)

    def get_batch(self, info_batch):
        self.info_batch = info_batch

    def pre_process(self):
        """
        info_batch => data_batch
        """
        raise NotImplementedError

    def forward(self):
        if 'mxnet' in self.config.engine or 'pytorch' in self.config.engine:
            self.engine.data_batch = self.data_batch
        elif 'tensorflow' in self.config.engine:
            self.engine.feed_dict = self.feed_dict
            self.engine.fetch_dict = self.fetch_dict
        else:
            raise NotImplementedError
        self.engine.forward()
        self.network_outputs = self.engine.network_outputs

    def post_process(self):
        """
        network_outputs => roidb
        """
        raise NotImplementedError

    def save_result(self):
        raise NotImplementedError

    def get_batch_list(self):
        return self.source.get_roidb_batch(int(self.config.batch_size))

    def run(self):
        info_batch_list = self.get_batch_list()
        for ind, info_batch in enumerate(info_batch_list):
            logging.info("%s: %d / %d (num_batch)" % (self.task_name, ind, len(info_batch_list)))
            self.get_batch(info_batch)
            self.pre_process()
            self.forward()
            self.post_process()
            self.save_result()


def load_param(param_path):
    import mxnet as mx
    save_dict = mx.nd.load(param_path)
    arg_params = {}
    aux_params = {}
    for k, v in save_dict.items():
        tp, name = k.split(':', 1)
        if tp == 'arg':
            arg_params[name] = v
        if tp == 'aux':
            aux_params[name] = v
    return arg_params, aux_params
