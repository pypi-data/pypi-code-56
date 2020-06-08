import pickle
import re
import gzip
import sys
import argparse
import json
import random
import logging
import warnings
import numpy
import torch
from starcoder.dataset import Missing, Unknown


warnings.filterwarnings("ignore")


class Scheduler(torch.optim.lr_scheduler.ReduceLROnPlateau):
    def __init__(self, early_stop, *argv, **argdict):
        self.early_stop = early_stop
        self.num_bad_epochs_for_early_stop = 0
        super(Scheduler, self).__init__(*argv, **argdict)
        
    def step(self, metrics, epoch=None):
        is_reduce_rate = False
        is_early_stop = False
        is_new_best = False
        # convert `metrics` to float, in case it's a zero-dim Tensor
        current = float(metrics)
        if epoch is None:
            epoch = self.last_epoch + 1
        else:
            warnings.warn(EPOCH_DEPRECATION_WARNING, UserWarning)
        self.last_epoch = epoch

        if self.is_better(current, self.best):
            self.best = current
            is_new_best = True
            self.num_bad_epochs = 0
            self.num_bad_epochs_for_early_stop = 0
        else:
            self.num_bad_epochs += 1
            self.num_bad_epochs_for_early_stop += 1

        if self.in_cooldown:
            self.cooldown_counter -= 1
            self.num_bad_epochs = 0  # ignore any bad epochs in cooldown
            self.num_bad_epochs_for_early_stop = 0

        if self.num_bad_epochs > self.patience:
            self._reduce_lr(epoch)
            self.cooldown_counter = self.cooldown
            self.num_bad_epochs = 0
            is_reduce_rate = True

        if self.num_bad_epochs_for_early_stop > self.early_stop:
            is_early_stop = True

        self._last_lr = [group['lr'] for group in self.optimizer.param_groups]
        return (is_reduce_rate, is_early_stop, is_new_best)
    

def compute_losses(entities, reconstructions, spec, field_models):
    """
    Gather and return all the field losses in a dictionary.
    """
    losses = {}
    for field_name, entity_values in entities.items():
        #print(field_name)
        if field_name in reconstructions and field_name not in [spec.id_field, spec.entity_type_field] + list(spec.relation_field_names):
            mask = entity_values > 0
            field_type = type(spec.field_object(field_name))
            reconstruction_values = reconstructions[field_name]
            recon = torch.reshape(reconstruction_values, (reconstruction_values.shape[0], -1)).sum(1)
            selector = torch.masked_select(torch.arange(0, entity_values.shape[0]),
                                           ~torch.isnan(entity_values) & ~torch.isnan(recon))
            losses[field_type] = losses.get(field_type, {})
            masked_entity_values = torch.index_select(entity_values, 0, selector) #~torch.isnan(entity_values))

            masked_reconstruction_values = torch.index_select(reconstruction_values, 0, selector) #~torch.isnan(entity_values))
            #print(masked_entity_values.dtype, masked_reconstruction_values.dtype, field_models[field_type][2])
            masked_field_losses = field_models[field_type][2](masked_reconstruction_values, masked_entity_values)
            losses[field_type][field_name] = masked_field_losses
    return losses


def tensorize(vals, field_obj):
    if any([isinstance(v, list) for v in vals]):
        max_length = max([len(v) for v in vals if isinstance(v, list)])
        vals = [(v + ([Missing.value] * (max_length - len(v)))) if v != None else [Missing.value] * max_length for v in vals]
    elif any([isinstance(v, (str,)) for v in vals]):
        return numpy.array(vals)
    else:
        vals = [(field_obj.missing_value if v == None else v) for v in vals]
    return torch.tensor(vals, dtype=field_obj.encoded_type)


def stack_batch(components, spec):
    lengths = [len(x) for x, _ in components]
    entities = sum([x for x, _ in components], [])
    adjacencies = [x for _, x in components]
    full_adjacencies = {}
    start = 0
    for l, adjs in zip(lengths, adjacencies):
        for name, adj in adjs.items():
            full_adjacencies[name] = full_adjacencies.get(name, numpy.full((len(entities), len(entities)), False))
            full_adjacencies[name][start:start + l, start:start + l] = adj.todense()
        start += l
    field_names = spec.field_names #regular_field_names #set(sum([[k for k in e.keys()] for e in entities], []))
    #field_names.add(spec.id_field)
    full_entities = {k : [] for k in field_names}
    for entity in entities:
        for field_name in field_names:
            full_entities[field_name].append(entity.get(field_name, None))
    #full_entities = {k : tensorize(v, spec.field_object(k)) for k, v in full_entities.items()}
    full_entities = {k : numpy.array(v) if k in spec.relation_fields else tensorize(v, spec.field_object(k)) for k, v in full_entities.items()}
    ne = len(entities)
    for k, v in full_adjacencies.items():
        a, b = v.shape
        assert(ne == a and ne == b)
    return (full_entities, {k : torch.tensor(v) for k, v in full_adjacencies.items()})


def split_batch(entities, adjacencies, count):
    ix = list(range(len(entities)))
    random.shuffle(ix)
    first_ix = ix[0:count]
    second_ix = ix[count:]
    first_entities = [entities[i] for i in first_ix]
    second_entities = [entities[i] for i in second_ix]
    first_adjacencies = {}
    second_adjacencies = {}
    for rel_type, adj in adjacencies.items():
        adjacencies[rel_type] = adj[first_ix, :][:, first_ix]
        adjacencies[rel_type] = adj[second_ix, :][:, second_ix]
    return ((first_entities, first_adjacencies), (second_entities, second_adjacencies))



#
# This has some unpleasantly-complicated logic for different ways of 
# handling components that don't fit into a batch:
#
#   "strict" means "never create an oversized batch"
#   "subselect" means "it's OK to split components over multiple batches"
#
# If strict=True and subselect=False, components larger than the
# batch size will never be seen, partial or otherwise.
#
def batchify(data, batch_size, strict=True, subselect=False, mask_tests=[]):
    component_ids = range(data.num_components)
    _component_ids = [c for c in component_ids]
    random.shuffle(_component_ids)
    current_batch = []
    current_total = 0
    for component_id in _component_ids:
        full_entities, adjacencies = data.component(component_id)
        masked_entities = []
        for e in full_entities:
            masked_entities.append(e.copy())
            for k in list(e.keys()):
                for mask_test in mask_tests:
                    if mask_test(e, k):
                        del masked_entities[-1][k]
        full_encoded_entities = [data.encode(e) for e in full_entities]
        masked_encoded_entities = [data.encode(e) for e in masked_entities]
        encoded_entities = list(zip(full_encoded_entities, masked_encoded_entities))

        while len(encoded_entities) > 0:
            if len(encoded_entities) > batch_size and subselect == False:
                # component is larger than batch size and not subselecting
                if strict == False:
                    # if not strict, just yield it
                    yield(
                        (
                            stack_batch([([x for x, _ in encoded_entities], adjacencies)], data._spec),
                            stack_batch([([x for _, x in encoded_entities], adjacencies)], data._spec)
                        )
                    )
                entities = []                    
            elif current_total + len(encoded_entities) > batch_size:
                # component + current is larger than batch size
                if subselect == True:
                    (sub_encoded_entities, sub_adjacencies), (encoded_entities, adjacencies) = split_batch(encoded_entities, 
                                                                                                           adjacencies, 
                                                                                                           batch_size - current_total)
                    current_batch.append((sub_encoded_entities, sub_adjacencies))
                    yield(
                        (
                            stack_batch([([x for x, _ in c], a) for c, a in current_batch], data._spec),
                            stack_batch([([x for _, x in c], a) for c, a in current_batch], data._spec)
                        )
                    )
                    #yield(stack_batch(current_batch, data._spec))
                    current_batch, current_total = [], 0
                else:
                    yield(
                        (
                            stack_batch([([x for x, _ in c], a) for c, a in current_batch], data._spec),
                            stack_batch([([x for _, x in c], a) for c, a in current_batch], data._spec)
                        )
                    )
                    current_batch, current_total = [], 0
            else:
                # component + current not large enough yet
                current_batch.append((encoded_entities, adjacencies))
                current_total += len(encoded_entities)
                encoded_entities = []
    if len(current_batch) > 0:
        # final batch
        yield(
            (
                stack_batch([([x for x, _ in c], a) for c, a in current_batch], data._spec),
                stack_batch([([x for _, x in c], a) for c, a in current_batch], data._spec)
            )
        )


def run_over_components(model, field_models, optim, loss_policy, data, batch_size, gpu, train, subselect=False, strict=True, mask_tests=[]):
    old_mode = model.training
    model.train(train)
    loss_by_field = {}
    loss = 0.0
    for ((full_entities, full_adjacencies), (masked_entities, masked_adjacencies)) in batchify(data, batch_size, subselect=subselect, strict=strict, mask_tests=mask_tests):
        batch_loss_by_field = {}
        if gpu:
            entities = {k : v.cuda() for k, v in entities.items()}
            adjacencies = {k : v.cuda() for k, v in adjacencies.items()}
        optim.zero_grad()
        reconstructions, bottlenecks, ae_pairs = model(masked_entities, masked_adjacencies)
        for field_type, fields in compute_losses(full_entities, reconstructions, data._spec, field_models).items():
            for field_name, losses in fields.items():
                batch_loss_by_field[(field_name, field_type)] = losses
        batch_loss = loss_policy(batch_loss_by_field, ae_pairs)
        loss += batch_loss
        if train:
            batch_loss.backward()
            optim.step()
        for k, v in batch_loss_by_field.items():
            loss_by_field[k] = loss_by_field.get(k, [])
            loss_by_field[k].append(v.clone().detach())
    model.train(old_mode)
    return (loss, loss_by_field)


def run_epoch(model, field_models, optimizer, loss_policy, train_data, dev_data, batch_size, gpu, mask_tests=[]):
    model.train(True)
    train_loss, train_loss_by_field = run_over_components(model, 
                                                          field_models, 
                                                          optimizer, 
                                                          loss_policy,
                                                          train_data, 
                                                          batch_size, 
                                                          gpu, 
                                                          train=True,
                                                          mask_tests=mask_tests,
    )
    model.train(False)
    dev_loss, dev_loss_by_field = run_over_components(model, 
                                                      field_models, 
                                                      optimizer, 
                                                      loss_policy,
                                                      dev_data, 
                                                      batch_size, 
                                                      gpu, 
                                                      train=False,
                                                      mask_tests=mask_tests,
    )

    return (train_loss.clone().detach().cpu(), 
            {k : [v.clone().detach().cpu() for v in vv] for k, vv in train_loss_by_field.items()},
            dev_loss.clone().detach().cpu(),
            {k : [v.clone().detach().cpu() for v in vv] for k, vv in dev_loss_by_field.items()})
