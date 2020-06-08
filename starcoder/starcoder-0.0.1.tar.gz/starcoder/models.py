import pickle
import re
import sys
import argparse
import torch
import json
import numpy
import scipy.sparse
import gzip
from torch.utils.data import DataLoader, Dataset
import functools
import numpy
import random
import logging
from torch.optim import Adam, SGD
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import torch.nn.functional as F
from starcoder.dataset import NumericField, DistributionField, CategoricalField, SequentialField, IntegerField, DateField, Missing, Unknown


# (batch_count x (entity_representation_size + (bottleneck_size * relation_count)) :: Float) -> (batch_count x entity_representation_size :: Float)
class Autoencoder(torch.nn.Module):
    def __init__(self, sizes, activation):
        super(Autoencoder, self).__init__()
        self._encoding_layers = []
        self._decoding_layers = []
        for i in range(len(sizes) - 1):
            f = sizes[i] if isinstance(sizes[i], int) else sum(sizes[i])
            t = sizes[i + 1] if isinstance(sizes[i + 1], int) else sum(sizes[i + 1])
            a = sizes[i] if isinstance(sizes[i], int) else sizes[i][0]
            self._encoding_layers.append(torch.nn.Linear(f, t))
            self._decoding_layers.append(torch.nn.Linear(t, a))
        self._encoding_layers = [torch.nn.Identity()] if len(self._encoding_layers) == 0 else self._encoding_layers
        self._decoding_layers = [torch.nn.Identity()] if len(self._decoding_layers) == 0 else self._decoding_layers
        self._encoding_layers = torch.nn.ModuleList(self._encoding_layers)
        self._decoding_layers = torch.nn.ModuleList(reversed(self._decoding_layers))
        self._loss = torch.nn.MSELoss()
        self._activation = activation()
        #self._dropout = torch.nn.Dropout(p=0.5)
    def forward(self, x):
        y = x.clone()
        #x = self._dropout(x)
        for layer in self._encoding_layers:
            x = self._activation(layer(x)) #torch.nn.functional.leaky_relu(layer(x))
        bottleneck = x.clone().detach()
        for layer in self._decoding_layers:
            x = self._activation(layer(x)) #torch.nn.functional.leaky_relu(layer(x))
        return (x, bottleneck, self._loss(x, y))
    @property
    def input_size(self):
        return self._encoding_layers[0].in_features    
    @property
    def output_size(self):
        return self._decoding_layers[-1].out_features        


#
class Projector(torch.nn.Module):

    def __init__(self, input_size, output_size, activation):
        super(Projector, self).__init__()
        self._layer = torch.nn.Linear(input_size, output_size)

    def forward(self, x):
        return torch.nn.functional.leaky_relu(self._layer(x))


# (batch_size :: Int) -> (batch_size x field_representation_size :: Float)
class CategoricalEncoder(torch.nn.Module):
    def __init__(self, field, activation, **args):
        super(CategoricalEncoder, self).__init__()
        self._embeddings = torch.nn.Embedding(num_embeddings=len(field), embedding_dim=args.get("embedding_size", 32))

    def forward(self, x):
        #print(x.shape)
        #print(self._embeddings.num_embeddings)
        retval = self._embeddings(x) #.long())
        #print(retval)
        return(retval)

    @property
    def input_size(self):
        return 1

    @property
    def output_size(self):
        return self._embeddings.embedding_dim


# (batch_size x entity_representation_size :: Float) -> (batch_size x item_types :: Float)
class CategoricalDecoder(torch.nn.Module):
    def __init__(self, field, input_size, activation, **args): #input_size):
        super(CategoricalDecoder, self).__init__()
        output_size = len(field)
        self._layerA = torch.nn.Linear(input_size, output_size)
        self._layerB = torch.nn.Linear(output_size, output_size)
    def forward(self, x):
        x = torch.nn.functional.leaky_relu(self._layerA(x))
        x = self._layerB(x)
        x = torch.nn.functional.log_softmax(x, dim=1)
        return x
    @property
    def input_size(self):
        return self._layer.in_features
    @property
    def output_size(self):
        return self._layer.out_features        


CategoricalLoss = torch.nn.NLLLoss


# (batch_count :: Float) -> (batch_count :: Float)
class NumericEncoder(torch.nn.Module):
    def __init__(self, field, activation, **args):
        super(NumericEncoder, self).__init__()
    def forward(self, x):
        retval = torch.as_tensor(torch.unsqueeze(x, 1), dtype=torch.float32, device=x.device)
        return retval
    @property
    def input_size(self):
        return 1
    @property
    def output_size(self):
        return 1


# (batch_count x entity_representation_size :: Float) -> (batch_count :: Float)    
class NumericDecoder(torch.nn.Module):
    def __init__(self, field, input_size, activation, **args):
        super(NumericDecoder, self).__init__()
        self._linear = torch.nn.Linear(input_size, 1)
    def forward(self, x):
        retval = torch.nn.functional.leaky_relu(self._linear(x))
        retval = self._linear(torch.nn.functional.leaky_relu(x))
        return retval.squeeze()
    @property
    def input_size(self):
        return self._linear.in_features
    @property
    def output_size(self):
        return self._linear.out_features


NumericLoss = torch.nn.MSELoss


# (batch_count :: Float) -> (batch_count :: Float)
class DistributionEncoder(torch.nn.Module):
    def __init__(self, field, activation, **args):
        self._size = len(field._categories)
        super(DistributionEncoder, self).__init__()
    def forward(self, x):
        return x #torch.unsqueeze(x, 1)
    @property
    def input_size(self):
        return self._size
    @property
    def output_size(self):
        return self._size


# (batch_count x entity_representation_size :: Float) -> (batch_count :: Float)    
class DistributionDecoder(torch.nn.Module):
    def __init__(self, field, input_size, activation, **args):
        super(DistributionDecoder, self).__init__()
        self._linear = torch.nn.Linear(input_size, len(field._categories))
    def forward(self, x):
        return torch.nn.functional.log_softmax(torch.nn.functional.leaky_relu(self._linear(x)).squeeze(), dim=1)
    @property
    def input_size(self):
        return self._linear.in_features
    @property
    def output_size(self):
        return self._linear.out_features


DistributionLoss = torch.nn.KLDivLoss


# item_sequences -> lengths -> hidden_state
# (batch_count x max_length :: Int) -> (batch_count :: Int) -> (batch_count x entity_representation_size :: Float)
class SequentialEncoder(torch.nn.Module):
    def __init__(self, field, activation, **args):
        super(SequentialEncoder, self).__init__()
        es = args.get("embedding_size", 32)
        hs = args.get("hidden_size", 64)
        rnn_type = args.get("rnn_type", torch.nn.GRU)
        self._embeddings = torch.nn.Embedding(num_embeddings=len(field), embedding_dim=es)
        self._rnn = rnn_type(es, hs, batch_first=True, bidirectional=False)
    def forward(self, x):
        l = (x != Missing.value).sum(1)
        nonempty = l != 0
        x = x[nonempty]
        l = l[nonempty]
        embs = self._embeddings(x)
        pk = torch.nn.utils.rnn.pack_padded_sequence(embs, l, batch_first=True, enforce_sorted=False)
        output, h = self._rnn(pk)
        h = h.squeeze(0)
        retval = torch.zeros(size=(nonempty.shape[0], h.shape[1]), device=l.device)
        mask = nonempty.unsqueeze(1).expand((nonempty.shape[0], h.shape[1]))
        retval.masked_scatter_(mask, h)
        return retval
    @property
    def input_size(self):
        return self._rnn.input_size
    @property
    def output_size(self):
        return self._rnn.hidden_size


# representations -> item_distributions
# (batch_count x entity_representation_size :: Float) -> (batch_count x max_length x item_types :: Float)
class SequentialDecoder(torch.nn.Module):
    def __init__(self, field, input_size, activation, **args): #hidden_size, rnn_type=torch.nn.GRU):
        super(SequentialDecoder, self).__init__()
        hs = args.get("hidden_size", 128)
        rnn_type = args.get("rnn_type", torch.nn.GRU)
        self._max_length = field._max_length
        self._rnn = rnn_type(input_size, hs, batch_first=True, bidirectional=False)
        self._classifier = torch.nn.Linear(hs, len(field))
    def forward(self, x):
        x = torch.stack([x for i in range(self._max_length)], dim=1)
        output, _ = self._rnn(x)
        outs = []
        for i in range(self._max_length):
            outs.append(torch.nn.functional.log_softmax(self._classifier(output[:, i, :]), dim=1))
        return torch.stack(outs, 1)
    @property
    def input_size(self):
        return self._rnn.input_size
    @property
    def output_size(self):
        return self._rnn.hidden_size


class SequentialLoss(object):
    def __init__(self, reduction):
        self._nll = torch.nn.NLLLoss(reduction=reduction)
    def __call__(self, x, target):
        x = x[:, 0:target.shape[1], :]
        losses = []
        for v in range(target.shape[1]):
            losses.append(self._nll(x[:, v, :], target[:, v]))
        return torch.cat(losses)


# representations -> summary
# (related_entity_count x bottleneck_size) -> (bottleneck_size)
class RNNSummarizer(torch.nn.Module):
    def __init__(self, input_size, activation, rnn_type=torch.nn.GRU):
        super(RNNSummarizer, self).__init__()
        self._rnn = rnn_type(input_size, input_size, batch_first=True)
    def forward(self, representations):
        out, h = self._rnn(representations.unsqueeze(0))
        return h.squeeze()

class MaxPoolSummarizer(torch.nn.MaxPool1d):
    def __init__(self, input_size, activation):
        super(MaxPoolSummarizer, self).__init__(1)
    def forward(self, x):
        return super(MaxPoolSummarizer, self).forward(x)

class SingleSummarizer(torch.nn.Identity):
    def __init__(self, input_size, activation):
        self._input_size = input_size
        super(SingleSummarizer, self).__init__()
    def forward(self, x):
        if x.shape[0] == 0:
            return torch.zeros(shape=(self._input_size,))
        else:
            return x[0]
        

    
#class DummyAutoencoder(torch.nn.Identity):
#    def __init__(self):
#        super(DummyAutoencoder, self).__init__()
#    def forward(self, x):
#        return (x, None, None)


#class DummyProjector(torch.nn.Identity):
#    def __init__(self, size):
#        super(DummyProjector, self).__init__()
#        self._size = size
#    def forward(self, x):
#        return torch.zeros(size=(x.shape[0], self._size), device=x.device)

#class IdentityProjector(torch.nn.Identity):
#    pass

class MLPProjector(torch.nn.Module):
    def __init__(self, in_size, out_size, activation):
        super(MLPProjector, self).__init__()
        self._layer = torch.nn.Linear(in_size, out_size)
    def forward(self, x):
        return self._layer(x)

field_models = {
    NumericField : (NumericEncoder, NumericDecoder, NumericLoss(reduction="none")),
    DistributionField : (DistributionEncoder, DistributionDecoder, DistributionLoss(reduction="none")),
    IntegerField : (NumericEncoder, NumericDecoder, NumericLoss(reduction="none")),
    CategoricalField : (CategoricalEncoder, CategoricalDecoder, CategoricalLoss(reduction="none")),
    SequentialField : (SequentialEncoder, SequentialDecoder, SequentialLoss(reduction="none")),
    DateField : (NumericEncoder, NumericDecoder, NumericLoss(reduction="none")),
}


class GraphAutoencoder(torch.nn.Module):
    def __init__(self,
                 spec,
                 depth,
                 autoencoder_shapes,
                 embedding_size,
                 hidden_size,
                 field_dropout,
                 hidden_dropout,
                 summarizers=SingleSummarizer,
                 activation=torch.nn.ReLU,
                 projected_size=None):
        """
        """
        super(GraphAutoencoder, self).__init__()

        self._track_bottlenecks = {}
        
        self._device = torch.device('cpu')
        self._autoencoder_shapes = autoencoder_shapes

        self._field_dropout = field_dropout
        self._hidden_dropout = hidden_dropout
        self._embedding_size = embedding_size
        self._hidden_size = hidden_size
        self._bottleneck_size = None if autoencoder_shapes in [[], None] else autoencoder_shapes[-1]

        self._cache = {}
        
        # entity and field specification
        self._spec = spec

        # order in which to process entity-types
        self._entity_type_order = sorted(spec.entity_types)

        # order in which to process each entity-type's fields
        self._entity_type_field_order = {et : sorted([f for f in spec.entity_fields(et) if type(spec.field_object(f)) in field_models], key=lambda x : str(x)) for et in spec.entity_types}

        # list of non-ID/entity-type fields
        self._field_names = spec.data_field_names
        
        # order in which to process each entity-type's relations
        self._entity_type_relation_order = {et : sorted([x for x in spec.entity_relations(et)]) for et in spec.entity_types}
        
        # how many hops to propagate signal in the graph
        self._depth = depth        

        # encoded widths of entities
        self._boundary_sizes = {}

        # an encoder for each field
        self._field_encoders = {}
        for field_name in self._spec.field_names:
            field_type = type(self._spec.field_object(field_name))
            if field_type in field_models:
                self._field_encoders[field_name] = field_models[field_type][0](self._spec._field_name_to_object[field_name], activation)
        self._field_encoders = torch.nn.ModuleDict(self._field_encoders)

        for entity_type in self._entity_type_order:
            for field_name in self._entity_type_field_order[entity_type]:
                self._boundary_sizes[entity_type] = self._boundary_sizes.get(entity_type, 0)
                self._boundary_sizes[entity_type] += self._field_encoders[field_name].output_size

        #an autoencoder for each entity type and depth
        self._entity_autoencoders = {}        
        for entity_type in self._entity_type_order:
            boundary_size = self._boundary_sizes.get(entity_type, 0)
            self._entity_autoencoders[entity_type] = [Autoencoder([boundary_size] + self._autoencoder_shapes, activation)]
            for _ in self._spec.entity_relations(entity_type):
                boundary_size += self._bottleneck_size
            for depth in range(self._depth):
                self._entity_autoencoders[entity_type].append(Autoencoder([boundary_size] + self._autoencoder_shapes, activation))

            self._entity_autoencoders[entity_type] = torch.nn.ModuleList(self._entity_autoencoders[entity_type])
        self._entity_autoencoders = torch.nn.ModuleDict(self._entity_autoencoders)

        # a summarizer for each entity-to-entity relation
        if self._depth > 0:
            self._summarizers = {}
            for entity_type in self._entity_type_order:
                self._summarizers[entity_type] = {}
                for name in spec.entity_relations(entity_type):
                    self._summarizers[entity_type][name] = summarizers(self._bottleneck_size, activation)
                self._summarizers[entity_type] = torch.nn.ModuleDict(self._summarizers[entity_type])
            self._summarizers = torch.nn.ModuleDict(self._summarizers)

        # MLP for each entity type to project representations to a common size
        # note the largest boundary size
        self._projected_size = projected_size if projected_size != None else max(self._boundary_sizes.values())
        self._projectors = {}
        for entity_type in self._entity_type_order:
            boundary_size = self._boundary_sizes.get(entity_type, 0)
            for _ in self._spec.entity_relations(entity_type):
                boundary_size += self._bottleneck_size
            self._projectors[entity_type] = MLPProjector(boundary_size, self._projected_size, activation)
        self._projectors = torch.nn.ModuleDict(self._projectors)
        
        # a decoder for each field
        # change from per-entity-per-field to just per-field!
        self._field_decoders = {}
        for field_name in self._spec.field_names:
            field_type = type(self._spec.field_object(field_name))
            if field_type in field_models:
                self._field_decoders[field_name] = field_models[field_type][1](self._spec._field_name_to_object[field_name], self._projected_size, activation)
        self._field_decoders = torch.nn.ModuleDict(self._field_decoders)

    def cuda(self):
        self._device = torch.device('cuda:0')
        super(GraphAutoencoder, self).cuda()

    @property
    def entity_type_order(self):
        return self._entity_type_order
    
    @property
    def spec(self):
        return self._spec
        
    @property
    def id_field(self):
        return self.spec.id_field
    
    @property
    def device(self):
        return self._device

    @property
    def entity_type_field(self):
        return self.spec.entity_type_field

    @property
    def device(self):
        return self._device

    @property
    def entity_types(self):
        return self.spec.entity_types

    def encoder(self, field_name):
        return self._field_encoders[field_name]
    
    def forward(self, entities, adjacencies):
        logging.debug("Starting forward pass")

        num_entities = len(entities[self.id_field])
        entity_indices = {}
        field_indices = {}
        entity_field_indices = {}
        autoencoder_boundary_pairs = []

        logging.debug("Assembling entity, field, and (entity, field) indices")        
        index_space = torch.arange(0, entities[self.entity_type_field].shape[0], 1)
        for entity_type in self._entity_type_order:
            entity_mask = (entities[self.entity_type_field] == self._spec.field_object(self.entity_type_field)[entity_type])
            entity_indices[entity_type] = index_space.masked_select(entity_mask)
            for field_name in self._entity_type_field_order[entity_type]:
                field_mask = ~torch.isnan(torch.reshape(entities[field_name], (entities[field_name].shape[0], -1)).sum(1))
                field_indices[field_name] = index_space.masked_select(field_mask)
                entity_field_mask = entity_mask & field_mask
                entity_field_indices[(entity_type, field_name)] = index_space.masked_select(entity_field_mask)

        
        
        logging.debug("Encoding each input field to a fixed-length representation")
        field_encodings = {}
        for field_name in self.spec.data_field_names:
            field_encodings[field_name] = torch.full(size=(num_entities, self.encoder(field_name).output_size),
                                                     fill_value=0.0,
                                                     device=self.device,
                                                     dtype=torch.float32)
            indices = field_indices[field_name]
            field_values = torch.index_select(entities[field_name], 0, indices)
            field_encodings[field_name][indices] = self.encoder(field_name)(field_values)

        logging.debug("Constructing entity-autoencoder inputs by concatenating field encodings")
        autoencoder_inputs = {}
        for entity_type, indices in entity_indices.items():
            #
            # each appended value should have shape (entity_count x encoding_width)
            #
            autoencoder_inputs[entity_type] = []
            for field_name in self._entity_type_field_order[entity_type]:
                #ef_key = (entity_type, field_name)                
                # should missing values be 0, NaN...?
                #fill_value = 0 # float("nan") # self._spec.field_object(field_name).missing_value
                #encodings = torch.full(size=(num_entities, self._field_encoders[field_name].output_size),
                #                       fill_value=fill_value,
                #                       device=self._device, dtype=torch.float32)
                #encodings = torch.full(size=(entity_index.shape[0], self._field_encoders[field_name].output_size),
                #                       fill_value=fill_value,
                #                       device=self._device, dtype=torch.float32)

                #field_values = torch.index_select(entities[field_name], 0, entity_field_indices[ef_key])
                #field_values = torch.index_select(entities[field_name], 0, entity_indices[entity_type])
                #print(field_name, field_values, entity_field_indices)
                #encodings[entity_field_indices[ef_key]] = self._field_encoders[field_name](field_values)
                #encodings[entity_field_indices[ef_key]] = self._field_encoders[field_name](field_values)
                autoencoder_inputs[entity_type].append(torch.index_select(field_encodings[field_name], 0, indices))
                #autoencoder_inputs[entity_type].append(torch.index_select(encodings)
            autoencoder_inputs[entity_type].append(torch.zeros(size=(indices.shape[0], 0), dtype=torch.float32, device=self._device))
            autoencoder_inputs[entity_type] = torch.cat(autoencoder_inputs[entity_type], 1)

        # always holds the most-recent autoencoder reconstructions
        autoencoder_outputs = {}

        # always holds the most-recent bottleneck representations
        bottlenecks = torch.zeros(size=(num_entities, self._bottleneck_size), device=self._device)

        # zero-depth autoencoder
        depth = 0
        logging.debug("Running %d-depth autoencoder", depth)
        for entity_type, entity_index in entity_indices.items():
            entity_outputs, bns, losses = self._entity_autoencoders[entity_type][0](autoencoder_inputs[entity_type])
            autoencoder_outputs[entity_type] = entity_outputs
            bottlenecks[entity_index] = bns

        # n-depth autoencoders
        prev_bottlenecks = bottlenecks.clone()
        for depth in range(1, self._depth + 1):
            logging.debug("Running %d-depth autoencoder", depth)            
            for entity_type, entity_index in entity_indices.items():
                autoencoder_outputs[entity_type] = autoencoder_outputs[entity_type].narrow(1, 0, self._entity_autoencoders[entity_type][0].output_size)
                other_reps = []
                for rel_name in self._entity_type_relation_order[entity_type]:
                    summarize = self._summarizers[entity_type][rel_name]
                    relation_reps = torch.zeros(size=(len(entity_indices[entity_type]), self._bottleneck_size), device=self._device)
                    for i, index in enumerate(entity_indices[entity_type]):
                        if rel_name not in adjacencies:
                            continue
                        related_indices = index_space.masked_select(adjacencies[rel_name][index])
                        if len(related_indices) > 0:
                            logging.debug("%d has %s-related indices %s", index, rel_name, related_indices)
                            obns = torch.index_select(prev_bottlenecks, 0, related_indices)
                            relation_reps[i] = summarize(obns)
                    other_reps.append(relation_reps)
                sh = list(autoencoder_outputs[entity_type].shape)
                sh[1] = 0
                other_reps = torch.cat(other_reps, 1) if len(other_reps) > 0 else torch.zeros(size=tuple(sh), device=self._device)
                autoencoder_inputs[entity_type] = torch.cat([autoencoder_outputs[entity_type], other_reps], 1)
                if depth > len(self._entity_autoencoders[entity_type]) - 1:
                    entity_outputs, bns, losses = self._entity_autoencoders[entity_type][-1](autoencoder_inputs[entity_type])
                else:
                    entity_outputs, bns, losses = self._entity_autoencoders[entity_type][depth](autoencoder_inputs[entity_type])
                autoencoder_outputs[entity_type] = entity_outputs
                bottlenecks[entity_index] = bns

        logging.debug("Projecting autoencoder outputs")
        if self._depth > 0:
            resized_autoencoder_outputs = {k : self._projectors[k](v) for k, v in autoencoder_outputs.items()}
        else:
            resized_autoencoder_outputs = {k : v for k, v in autoencoder_outputs.items()}
            
        # reconstruct the entities by unfolding the last autoencoder output
        logging.debug("Reconstructing the input by applying decoders to the autoencoder output")
        reconstructions = {}
        for entity_type, entity_index in entity_indices.items():
            logging.debug("\tFor '%s' entities", entity_type)
            for field_name in self._entity_type_field_order.get(entity_type, []):
                logging.debug("\t\tFor field '%s'", field_name)
                out = self._field_decoders[field_name](resized_autoencoder_outputs[entity_type])
                if field_name not in reconstructions:
                    reconstructions[field_name] = torch.zeros(size=[num_entities] + list(out.shape)[1:], device=self._device)
                reconstructions[field_name][entity_mask] = out
        reconstructions[self._spec.id_field] = entities[self._spec.id_field]
        reconstructions[self.entity_type_field] = entities[self.entity_type_field]
        for rel in self.spec.relation_field_names:
            reconstructions[rel] = entities[rel]
        logging.debug("Returning reconstructions, bottlenecks, and autoencoder I/O pairs")
        return (reconstructions, bottlenecks, autoencoder_boundary_pairs)

    # Recursively initialize model weights
    def init_weights(m):
        if type(m) == torch.nn.Linear or type(m) == torch.nn.Conv1d:
            torch.nn.init.xavier_uniform_(m.weight)
            m.bias.data.fill_(0.01)

