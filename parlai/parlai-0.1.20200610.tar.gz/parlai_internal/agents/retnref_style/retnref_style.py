#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import random
from itertools import chain

import numpy as np
import torch
from torch import nn as nn
from torch.nn import functional as F

from parlai.agents.transformer.modules import (
    TransformerDecoder,
    TransformerGeneratorModel,
    _normalize,
)
from parlai.agents.transformer.polyencoder import PolyencoderAgent
from parlai.agents.transformer.transformer import (
    TransformerClassifierAgent,
    TransformerGeneratorAgent,
)
from parlai.core.metrics import AverageMetric
from parlai.core.torch_agent import History, Output
from parlai.utils.fp16 import FP16SafeCrossEntropy
from parlai.utils.misc import AttrDict, warn_once, round_sigfigs
from parlai_internal.agents.bert_ranker_classifier.bert_ranker_classifier import (
    RankingClassificationMixin,
)
from parlai_internal.agents.retnref.retnref import RetnrefAgent, RetnrefHistory


RETRIEVAL_MODEL_FILE = '/checkpoint/ems/retrieve_st/sweeps_ems/s2020_03_09__imagechat_retriever/001/fd8_jobid=18/model'
RET_FCP = ''  # We pass in no candidate file to force using the train cands of our task
STYLE_SEP_TOKEN = ' STYLE '


"""
Example usage: (train on IGC generative task, finetuning model from dodeca)

python examples/train_model.py -t internal:comment_battle:ImageDialogGeneration -m internal:retnref_style --choose-label-pct 0.1 --init-model /checkpoint/parlai/zoo/new_reddit/newreddit_trained20190909_usedfordodeca/model --dict-file /checkpoint/parlai/zoo/new_reddit/newreddit_trained20190909_usedfordodeca/model.dict --embedding-size 512 --n-layers 8 --ffn-size 2048 --dropout 0.1 --n-heads 16 --learn-positional-embeddings True --n-positions 512 --variant xlm --activation gelu --skip-generation True --fp16 True --text-truncate 512 --label-truncate 128 --dict-tokenizer bpe --dict-lower True -lr 1e-06 --optimizer adamax --lr-scheduler reduceonplateau --gradient-clip 0.1 -veps 0.25 --betas 0.9,0.999 --update-freq 1 --attention-dropout 0.0 --relu-dropout 0.0 --skip-generation True -vp 15 -stim 60 -vme 5000 -bs 16 -vmt ppl -vmm min --save-after-valid True -mf /tmp/retnrefstyle --set-retriever-gpu False
"""


class StyleHistoryMixin(History):
    """
    Methods for adding style to history.
    """

    def __init__(self, opt, **kwargs):
        super().__init__(opt, **kwargs)
        self.use_style_frac = opt['use_style_frac']
        self.style = None

    def reset(self):
        super().reset()
        self.style = None

    def update_history(self, obs, *args, **kwargs):
        super().update_history(obs, *args, **kwargs)
        use_style_rand = random.random()
        if use_style_rand < self.use_style_frac:
            # Use the style
            self.style = obs.get('personality')
            # This key name is dependent on ImageChat and will change for other tasks.
            # If obs does not contain 'personality' (i.e. at the end of an epoch during
            # validation), there will be no style
            if self.style == '':
                self.style = None
        else:
            self.style = None

    def get_history_str(self):
        history_str = super().get_history_str()
        if history_str is not None and self.style is not None:
            history_str += STYLE_SEP_TOKEN + self.style

        return history_str

    def get_history_vec(self):
        history = super().get_history_vec()

        if history is not None and self.style is not None:
            style = STYLE_SEP_TOKEN + self.style
            style_tok = self.parse(style)
            if self.vec_type == 'deque':
                history.extend(style_tok)
            else:
                history += style_tok

        return history


class StyleAgentMixin:
    """
    Methods for agents that return style from their histories.
    """

    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add command-line arguments specifically for this agent. Does not add arguments
        from its superclass because it's a mixin.
        """
        agent = argparser.add_argument_group('Style arguments')
        agent.add_argument(
            '--use-style-frac',
            type=float,
            default=1.0,
            help='What fraction of the time to use the style label',
        )
        return agent


class RetnrefStyleHistory(StyleHistoryMixin, RetnrefHistory):
    """
    Modify history to save the style, in addition to the retriever's response.
    """

    def get_history_vec_no_ret(self):
        """
        Get the history response without the retriever or style.
        """
        hist = super(
            RetnrefHistory, self
        ).get_history_vec()  # call method from regular history class
        if hist is None:
            return []
        return hist


class RetnrefStyleAgent(StyleAgentMixin, RetnrefAgent):
    """
    General purpose retrieve and refine generator.
    """

    @classmethod
    def history_class(cls):
        """
        Determine the history class: this is useful for appending the style.
        """
        return RetnrefStyleHistory

    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add command-line arguments specifically for this agent.
        """
        StyleAgentMixin.add_cmdline_args(argparser)
        RetnrefAgent.add_cmdline_args(argparser)
        argparser.set_defaults(ret_model_file=RETRIEVAL_MODEL_FILE, ret_fcp=RET_FCP)
        return argparser


class StyleHistory(StyleHistoryMixin, History):
    """
    Modify history to save the style, but without a retriever response. Also useful for
    the retriever (in which there is no retriever response from itself).
    """


class StyleControlAgent(StyleAgentMixin, TransformerGeneratorAgent):
    """
    General purpose generator with a style in the history.
    """

    @classmethod
    def history_class(cls):
        """
        Determine the history class in order to append the style.
        """
        return StyleHistory

    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add command-line arguments specifically for this agent.
        """
        StyleAgentMixin.add_cmdline_args(argparser)
        TransformerGeneratorAgent.add_cmdline_args(argparser)
        return argparser


class StylePolyencoderAgent(StyleAgentMixin, PolyencoderAgent):
    """
    Polyencoder with a style in the history.
    """

    @classmethod
    def history_class(cls):
        """
        Determine the history class in order to append the style.
        """
        return StyleHistory

    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add command-line arguments specifically for this agent.
        """
        StyleAgentMixin.add_cmdline_args(argparser)
        PolyencoderAgent.add_cmdline_args(argparser)
        return argparser


class ClassifierOnGeneratorAgent(RankingClassificationMixin, TransformerGeneratorAgent):
    """
    Agent that uses a generator model with a classifier head.

    Useful for performing classification with a pretrained generator model. Note that
    generator encoder/decoder weights will be frozen during classifier training.
    """

    # TODO: reduce amount of code duplicated from TorchClassifierAgent

    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add CLI args.
        """
        TransformerClassifierAgent.add_cmdline_args(argparser)
        agent = argparser.add_argument_group('GeneratorWithClassifierHead Arguments')
        agent.add_argument(
            '--freeze-enc-dec-weights',
            type='bool',
            default=False,
            help='Only train the classifier head and not the encoder and decoder',
        )
        agent.add_argument(
            '--personality-as-label',
            type='bool',
            default=True,
            help='The personality is in the label field instead of the personality field',
        )
        return agent

    def __init__(self, opt, shared=None):
        """
        Set up model.
        """

        # set up classes
        if opt.get('classes') is None and opt.get('classes_from_file') is None:
            raise RuntimeError(
                'Must specify --classes or --classes-from-file argument.'
            )
        if not shared:
            if opt['classes_from_file'] is not None:
                with open(opt['classes_from_file']) as f:
                    self.class_list = f.read().splitlines()
            else:
                self.class_list = opt['classes']
            self.class_dict = {val: i for i, val in enumerate(self.class_list)}
            if opt.get('class_weights', None) is not None:
                self.class_weights = opt['class_weights']
            else:
                self.class_weights = [1.0 for _ in self.class_list]
        else:
            self.class_list = shared['class_list']
            self.class_dict = shared['class_dict']
            self.class_weights = shared['class_weights']

        self.personality_as_label = opt['personality_as_label']

        super().__init__(opt, shared)

        # Override the criterion
        if not shared:
            self.criterion = self.build_criterion()
            if self.use_cuda:
                self.criterion.cuda()

        # Freeze generator encoder/decoder weights
        if opt['freeze_enc_dec_weights']:
            for param in chain(
                self.model.encoder.parameters(), self.model.decoder.parameters()
            ):
                param.requires_grad = False

    def build_model(self, states=None):
        """
        Build and return model.
        """
        model = ClassifierOnGeneratorModel(
            self.opt,
            self.dict,
            num_classes=len(self.class_list),
            personality_as_label=self.personality_as_label,
        )
        return model

    def build_criterion(self):
        weight_tensor = torch.FloatTensor(self.class_weights)
        if not self.fp16:
            return torch.nn.CrossEntropyLoss(weight=weight_tensor, reduction='none')
        else:
            # FP16 safe cross entropy (softmax done in FP32)
            return FP16SafeCrossEntropy(weight=weight_tensor, reduction='none')

    def load_state_dict(self, state_dict):
        """
        Override to add in the classifier head if it doesn't exist.
        """
        for tensor in ['weight', 'bias']:
            key = f'classifier_head.{tensor}'
            if key not in state_dict:
                state_dict[key] = getattr(self.model.classifier_head, tensor)
        super().load_state_dict(state_dict)

    def share(self):
        """
        Share model parameters.
        """
        shared = super().share()
        shared['class_dict'] = self.class_dict
        shared['class_list'] = self.class_list
        shared['class_weights'] = self.class_weights
        return shared

    def batchify(self, obs_batch, sort=False):
        base_batch = super().batchify(obs_batch, sort)
        if self.personality_as_label:
            return base_batch
        else:
            assert sort is False
            # Sorting would make it hard to line up the observations within one batch
            personalities = [
                obs['personality'] for obs in obs_batch if self.is_valid(obs)
            ]
            assert len(personalities) == len(base_batch.text_vec)
            batch_with_personalities = BatchWithPersonalities(
                personalities=personalities, **base_batch.__dict__
            )
            return batch_with_personalities

    def _get_label_tensor(self, batch):
        """
        Obtain the correct class labels.

        Raises a `KeyError` if one of the labels is not in the class list.
        """
        if self.personality_as_label:
            labels = batch.labels
        else:
            labels = batch.personalities
        try:
            labels_indices_list = [self.class_dict[label] for label in labels]
        except KeyError as e:
            warn_once('One of your labels is not in the class list.')
            raise e

        labels_tensor = torch.LongTensor(labels_indices_list)
        if self.use_cuda:
            labels_tensor = labels_tensor.cuda()
        return labels_tensor

    def _format_interactive_output(self, probs, prediction_id):
        """
        Format interactive mode output with scores.
        """
        preds = []
        for i, pred_id in enumerate(prediction_id.tolist()):
            prob = round_sigfigs(probs[i][pred_id], 4)
            preds.append(
                'Predicted class: {}\nwith probability: {}'.format(
                    self.class_list[pred_id], prob
                )
            )
        return preds

    def batch_act(self, observations):
        """
        Overwriting RankingClassificationMixin.batch_act() in the case where the labels
        are stored in the "personality" field.
        """

        if self.personality_as_label:

            batch_reply = super().batch_act(observations)
            return batch_reply

        else:

            batch_reply = super(RankingClassificationMixin, self).batch_act(
                observations
            )

            labels = 'personality'

            preds = self._get_preds(batch_reply)

            if preds is None:
                return batch_reply

            labels_lst = [[label] for label in self._get_labels(observations, labels)]
            # The label is expected to be in a list like in the "labels" or
            # "eval_labels" fields

            self._update_confusion_matrix(preds, labels_lst)

            return batch_reply

    def train_step(self, batch):
        """
        Train on a single batch of examples.
        """
        if batch.text_vec is None:
            return Output()
        self.model.train()
        self.zero_grad()

        # Calculate loss
        labels = self._get_label_tensor(batch)
        scores = self.score(batch)
        loss = self.criterion(scores, labels)
        self.record_local_metric('loss', AverageMetric.many(loss))
        loss = loss.mean()
        self.backward(loss)
        self.update_params()

        # Get predictions
        _, prediction_id = torch.max(scores.float().cpu(), 1)
        preds = [self.class_list[idx] for idx in prediction_id]

        return Output(preds)

    def eval_step(self, batch):
        """
        Train on a single batch of examples.
        """
        if batch.text_vec is None:
            return

        self.model.eval()
        scores = self.score(batch)
        probs = F.softmax(scores, dim=1)
        _, prediction_id = torch.max(probs.float().cpu(), 1)
        preds = [self.class_list[idx] for idx in prediction_id]

        if batch.labels is None or self.opt['ignore_labels']:
            # interactive mode
            if self.opt.get('print_scores', False):
                preds = self._format_interactive_output(probs, prediction_id)
        else:
            labels = self._get_label_tensor(batch)
            loss = self.criterion(scores, labels)
            self.record_local_metric('loss', AverageMetric.many(loss))

        if self.opt.get('print_scores', False):
            return Output(preds, probs=probs.cpu())
        else:
            return Output(preds)

    def score(self, batch):
        return self.model(*self._model_input(batch))

    def _model_input(self, batch):
        """
        Create the input (x) value for the model.
        # TODO: explain the two cases!
        """
        if self.personality_as_label:
            return (batch.text_vec,)
        else:
            return batch.text_vec, batch.label_vec


class ClassifierOnGeneratorModel(TransformerGeneratorModel):
    """
    TransformerGeneratorModel with a classifier head on top of the decoder.

    Useful for performing classification with a pretrained generator model.
    """

    @classmethod
    def build_decoder(
        cls,
        opt,
        dictionary,
        embedding=None,
        padding_idx=None,
        n_positions=1024,
        n_segments=0,
    ):
        """
        Return TransformerDecoderWithEmbeds instead of TransformerDecoder.
        """
        n_layers = (
            opt['n_decoder_layers']
            if opt.get('n_decoder_layers', -1) > 0
            else opt['n_layers']
        )
        return TransformerDecoderWithEmbeds(
            n_heads=opt['n_heads'],
            n_layers=n_layers,
            embedding_size=opt['embedding_size'],
            ffn_size=opt['ffn_size'],
            vocabulary_size=len(dictionary),
            embedding=embedding,
            dropout=opt['dropout'],
            attention_dropout=opt['attention_dropout'],
            relu_dropout=opt['relu_dropout'],
            padding_idx=padding_idx,
            learn_positional_embeddings=opt['learn_positional_embeddings'],
            embeddings_scale=opt['embeddings_scale'],
            n_positions=n_positions,
            activation=opt['activation'],
            variant=opt['variant'],
            n_segments=n_segments,
        )

    def __init__(self, opt, dictionary, num_classes: int, personality_as_label: bool):
        super().__init__(opt, dictionary)
        self.classifier_head = nn.Linear(opt['embedding_size'], num_classes)
        self.personality_as_label = personality_as_label

    def forward(self, *xs):
        """
        Get output class logits from the model.

        :param xs:
            - list of inputs to the encoder/decoder. Elements:
              - text_vec: (LongTensor[bsz, text seqlen])
              - label_vec: (LongTensor[bsz, label seqlen])
                  (Only used if not self.personality_as_label)
        :return:
            - the model's predicted per-class scores.
              (FloatTensor[bsz, len(class_list)])
        """

        if self.personality_as_label:
            # All tokens go into the encoder and classification is learned from that.
            assert len(xs) == 1
            # Only one input allowed
            bsz = xs[0].size(0)
            encoder_states = self.encoder(*xs)
            inputs = self.START.detach().expand(bsz, 1)
            # Generate most likely class given start token as input
            latent, _ = self.decoder(inputs, encoder_states)
            # latent: [bsz, seqlen, emb_dim]
            scores = self.classifier_head(latent.squeeze(dim=1))
        else:
            # Tokens are split between the encoder and decoder and classification is
            # learned from both.
            text_vec, label_vec = xs
            encoder_states = self.encoder(text_vec)
            latent, _ = self.decoder(label_vec, encoder_states)
            # latent: [bsz, seqlen, emb_dim]
            scores = self.classifier_head(latent.mean(dim=1))

        return scores


class BatchWithPersonalities(AttrDict):
    """
    TODO: docstring
    """

    def __init__(self, personalities=None, **kwargs):
        super().__init__(personalities=personalities, **kwargs)


class TransformerDecoderWithEmbeds(TransformerDecoder):
    def forward(self, input, encoder_state, embedded_input=None, incr_state=None):
        """
        Forward pass with the ability to pass in token-embedded inputs.
        """
        # TODO: most of this is copied-and-pasted from TransformerDecoder.forward
        encoder_output, encoder_mask = encoder_state

        if input is not None:
            seq_len = input.size(1)
            positions = input.new(seq_len).long()
        else:
            seq_len = embedded_input.size(1)
            positions = embedded_input.new(seq_len).long()
        positions = torch.arange(seq_len, out=positions).unsqueeze(0)

        if incr_state is not None:
            # We're doing incremental decoding, so select only the most recent position
            if input is not None:
                input = input[:, -1:]
            if embedded_input is not None:
                embedded_input = embedded_input[:, -1:, :]
            if positions is not None:
                positions = positions[:, -1:]
        else:
            incr_state = {}

        if embedded_input is not None:
            tensor = embedded_input  # No need to copy because we only reassign below
        else:
            tensor = self.embeddings(input)
        if self.embeddings_scale:
            tensor = tensor * np.sqrt(self.dim)
        if self.variant == 'xlm':
            tensor = _normalize(tensor, self.norm_embeddings)
        if positions.max().item() > self.n_positions:
            warn_once(
                'You are inputting a sequence of {x} length, but only have '
                '--n-positions {y}. Set --truncate or increase --n-positions'.format(
                    x=positions.max().item(), y=self.n_positions
                )
            )
        tensor = tensor + self.position_embeddings(positions).expand_as(tensor)
        tensor = self.dropout(tensor)  # --dropout

        new_incr_state = {}
        if getattr(self.layers, 'is_model_parallel', False):
            tensor, new_incr_state = self._apply_model_parallel(
                tensor, encoder_output, encoder_mask, incr_state
            )
        else:
            for idx, layer in enumerate(self.layers):
                tensor, new_incr_state[idx] = layer(
                    x=tensor,
                    encoder_output=encoder_output,
                    encoder_mask=encoder_mask,
                    incr_state=incr_state.get(idx),
                )

        if self.variant == 'prelayernorm':
            tensor = _normalize(tensor, self.norm_embeddings)

        return tensor, new_incr_state
