import pickle
import re
import sys
import argparse
import json
import gzip
import functools
import random
import logging
import numpy
import scipy.sparse
from sklearn.metrics import f1_score, accuracy_score
from scipy.sparse.csgraph import connected_components
import torch
import math
import uuid
from starcoder import fields
# import time
# import calendar

# class Field(object):
#     def __init__(self, name, **args):
#         self.name = name
#         self.type_name = args["type"]
#     def encode(self, v):
#         return v
#     def decode(self, v):
#         return v
#     def observe_value(self, v):
#         pass
#     def __str__(self):
#         return "{1} field: {0}".format(self.name, self.type_name)
    
# class MetaField(Field):
#     def __init__(self, name, **args):
#         super(MetaField, self).__init__(name, **args)
    
# class DataField(Field):        
#     def __init__(self, name, **args):
#         super(DataField, self).__init__(name, **args)
    
# class EntityTypeField(MetaField):
#     def __init__(self, name, **args):
#         super(EntityTypeField, self).__init__(name, **args)

# class RelationField(MetaField):
#     def __init__(self, name, **args):
#         super(RelationField, self).__init__(name, **args)
#         self.target_entity_type = args["target_entity_type"]

# class IdField(MetaField):
#     def __init__(self, name, **args):
#         super(IdField, self).__init__(name, **args)
        
# class NumericField(DataField):    
#     def __init__(self, name, **args):
#         super(NumericField, self).__init__(name, **args)

# class IntegerField(DataField):    
#     def __init__(self, name, **args):
#         super(IntegerField, self).__init__(name, **args)
        
# class DateField(DataField):
#     def __init__(self, name, **args):
#         super(DateField, self).__init__(name, **args)
#     def encode(self, v):
#         t = time.strptime(v, "%d-%b-%Y")
#         return calendar.timegm(t)
#     def decode(self, v):
#         date = time.gmtime(v)
#         year = date.tm_year
#         month = calendar.month_abbr[date.tm_mon]
#         day = date.tm_mday
#         return "{}-{}-{}".format(day, month, year)
    
# class DistributionField(DataField):
#     def __init__(self, name, **args):
#         super(DistributionField, self).__init__(name, **args)

#     def encode(self, v):
#         total = sum(v.values())
#         return [0.0 if c not in v else (v[c] / total) for c in self._categories]

#     def decode(self, v):
#         assert(len(v) == len(self._categories))
#         retval = {}
#         if all([x >= 0 for x in v]):
#             total = sum([x for x in v])
#             for k, p in zip(self._categories, v):
#                 if p > 0:
#                     retval[k] = p / total
#         elif all([x <= 0 for x in v]):            
#             total = sum([math.exp(x) for x in v])
#             for k, p in zip(self._categories, v):
#                 retval[k] = math.exp(p) / total            
#         else:
#             raise Exception("Got probabilities that were not all of the same sign!")
#         return retval


# # class IntegerField(DataField):

# #     name = "numeric"

# #     def __init__(self, field_values):
# #         field_values = [float(x) for x in field_values]
# #         self._minimum = min(field_values)
# #         self._maximum = max(field_values)
# #         self._trivial = self._minimum == self._maximum

# #     def __str__(self):
# #         return "Integer(min/max={}/{})".format(self._minimum, self._maximum)

# #     def encode(self, v):
# #         return (0.0 if self._trivial else (v - self._minimum) / (self._maximum - self._minimum))

# #     def decode(self, v):
# #         return round(self._minimum if self._trivial else (v * (self._maximum - self._minimum) + self._minimum))


# class Missing(object):
#     pass

# class Unknown(object):
#     pass

    

# class CategoricalField(DataField):

#     #name = "categorical"
#     #missing_value = 0
#     #unknown_value = 1
#     #encoded_type = int
#     #na_value = 0
    
#     def __init__(self, name, **args):
#         super(CategoricalField, self).__init__(name, **args)
#         self._lookup = {} #Missing() : 0}
#         self._rlookup = {}
#         #self[Missing()] = self.missing_value #Missing.value
#         #self[Unknown()] = self.unknown_value
#         #for value in field_values:
#         #    self[value] = self.get(value, len(self))
#         #self._rlookup = {v : k for k, v in self.items()}

#     #def __str__(self):
#     #    return "Categorical(possible_values={})".format(len(self))

#     def observe_value(self, v):
#         i = self._lookup.setdefault(v, len(self._lookup))
#         self._rlookup[i] = v

    
#     def encode(self, v):
#         return self.get(v, self.unknown_value)

#     def decode(self, v):
#         if v not in self._rlookup:
#             raise Exception("Could not decode value '{0}' (type={2})".format(v, self._rlookup, type(v)))
#         return self._rlookup[v]
    
#     def __str__(self):
#         return "{1} field: {0}[{2}]".format(self.name, self.type_name, len(self._lookup))

# class SequentialField(DataField):

#     #name = "sequential"

#     def __init__(self, name, **args):
#         super(SequentialField, self).__init__(name, **args)
#         self._lookup = {}
#         self._rlookup = {}
#         #unique_sequences = set()
#         #self[Missing] = Missing.value
#         #self[Unknown] = Unknown.value
#         #self._max_length = 0
#         #for value in field_values:
#         #    unique_sequences.add(value)
#         #    self._max_length = max(self._max_length, len(value))
#         #    for element in value:
#         #        self[element] = self.get(element, len(self))
#         #self._rlookup = {v : k for k, v in self.items()}
#         #self._unique_sequence_count = len(unique_sequences)

#     #def __str__(self):
#     #    return "Sequential(unique_elems={}, unique_seqs={}, max_length={})".format(len(self),
#     #                                                                               self._unique_sequence_count, 
#     #                                                                               self._max_length)
#     def observe_value(self, vs):
#         for v in vs:
#             i = self._lookup.setdefault(v, len(self._lookup))
#             self._rlookup[i] = v
        
#     def __str__(self):
#         return "{1} field: {0}[{2}]".format(self.name, self.type_name, len(self._lookup))

#     def encode(self, v):
#         return [self.get(e, self[Unknown]) for e in v]

#     def decode(self, v):
#         try:
#             return "".join([self._rlookup[e] for e in v if e not in [Missing.value, Unknown.value]])
#         except:
#             raise Exception("Could not decode values '{0}' (type={2})".format(v, self._rlookup, type(v[0])))


# field_classes = {"numeric" : NumericField,
#                  "categorical" : CategoricalField,
#                  "boolean" : CategoricalField,                 
#                  "sequential" : SequentialField,
#                  #"integer" : IntegerField,
#                  "keyword" : CategoricalField,
#                  "text" : SequentialField,
#                  "relation" : RelationField,
#                  "distribution" : DistributionField,
#                  "date" : DateField,
#                  "id" : IdField,
#                  "entity_type" : EntityTypeField,
#              }


class Datum(dict):
    def __init__(self, schema, obj):
        self._meta_fields = {}
        self._data_fields = {}
        self._relation_fields = {}
        self._unknown_fields = {}
        for k, v in obj.items():
            pass

class EntityType(object):
    def __init__(self, name, data_fields, relation_fields):
        self.name = name
        self.data_fields = data_fields
        self.relation_fields = relation_fields
    def __str__(self):
        return "{}: data fields={}, relation fields={}".format(self.name, self.data_fields, self.relation_fields)

class Schema(object):
    def __init__(self, spec):
        self.id_field_name = spec["meta"]["id_field"]
        self.entity_type_field_name = spec["meta"]["entity_type_field"]
        self._field_objects = {self.id_field_name : fields.field_classes["id"](self.id_field_name),
                               self.entity_type_field_name : fields.field_classes["entity_type"](self.entity_type_field_name)
                               }
        self._entity_relation_field_names = {}
        self._entity_data_field_names = {}
        self._relation_field_names = set()
        self._data_field_names = set()        
        for field_name, field_spec in spec["data_fields"].items():
            field_type = field_spec["type"]
            self._data_field_names.add(field_name)
            self._field_objects[field_name] = field.field_classes[field_type](field_name, **field_spec)

        for entity_type, fields in spec["entity_types"].items():
            self._entity_data_field_names[entity_type] = set(fields)
            self._entity_relation_field_names[entity_type] = set()
            
        for field_name, field_spec in spec["relation_fields"].items():
            self._relation_field_names.add(field_name)
            self._entity_relation_field_names[entity_type].add(field_name)
            self._field_objects[field_name] = field_classes["relation"](field_name, type="relation", **field_spec)            

        self._entity_types = {}
        for entity_type, data_fields in self._entity_data_field_names.items():
            self._entity_types[entity_type] = EntityType(entity_type,
                                                         data_fields,
                                                         self._entity_relation_field_names.get(entity_type, []))

    @property
    def entity_type_field(self):
        return self._field_objects[self.entity_type_field_name]

    @property
    def id_field(self):
        return self._field_objects[self.id_field_name]

    @property
    def entity_types(self):
        return self._entity_types
            
    def __str__(self):
        return """
Schema(
    Fields:
        {}
        {} 
        {}
        {}
    entity types:
        {}
)
""".format(self._field_objects[self.id_field_name],
           self._field_objects[self.entity_type_field_name],
           "\n        ".join([str(self._field_objects[f]) for f in self._data_field_names]),
           "\n        ".join([str(self._field_objects[f]) for f in self._relation_field_names]),
           "\n        ".join([str(et) for et in self._entity_types.values()])
)

    def observe_entity(self, entity):
        for k, v in entity.items():
            #print(k)
            if k in self._field_objects:
                self._field_objects[k].observe_value(v)

                
    
    # def entity_relations(self, entity_type):
    #     return set([x for x in self.entity_fields(entity_type) if isinstance(self.field_object(x), RelationField)])

    # @property
    # def regular_field_names(self):
    #     return set([f for f, o in self._field_name_to_object.items() if not isinstance(o, (IdField, RelationField))])

    # @property
    # def entity_types(self):
    #     return set(self._entity_type_to_field_names.keys())

    # def entity_fields(self, entity_name):
    #     return self._entity_type_to_field_names.get(entity_name, set())

    # def field_object(self, field_name):
    #     return self._field_name_to_object[field_name]

    # def exists(self, field_name):
    #     return (field_name in self._field_name_to_object)

    # @property
    # def field_names(self):
    #     return set([f for f in self._field_name_to_object.keys()])

    # @property
    # def data_field_names(self):
    #     return set([f for f in self._field_name_to_object.keys() if f not in self._relation_fields and f not in [self._id_field, self._entity_type_field]])

    # @property
    # def data_fields(self):
    #     return set([f for f in self._field_name_to_object.keys() if f not in self._relation_fields and f not in [self._id_field, self._entity_type_field]])
           
    # @property
    # def entity_type_field(self):
    #     return self._entity_type_field

    # @property
    # def id_field_name(self):
    #     return self._id_field

    # @property
    # def id_field(self):
    #     return self._id_field

    # @property
    # def relation_field_names(self):
    #     return self._relation_fields

    # @property
    # def relation_fields(self):
    #     return self._relation_fields
           
    # @property
    # def has_id_field(self):
    #     return (self._id_field != None)

    # @property
    # def num_fields(self):
    #     return len(self._field_name_to_object)

    # @property
    # def num_entities(self):
    #     return len(self._entity_type_to_field_names)

    # @property
    # def num_relations(self):
    #     return sum([len(x) for x in self._entity_type_to_relation_types.values()])

    # def encode(self, datum):
    #     retval = {}
    #     for k, v in datum.items():
    #         if k in self.entity_relations(datum[self.entity_type_field]):
    #             retval[k] = self._field_name_to_object[self.id_field_name].encode(v)
    #         elif k not in self._field_name_to_object:
    #             retval[k] = v
    #         else:
    #             retval[k] = self._field_name_to_object[k].encode(v)
    #     return retval

    # def decode(self, datum):
    #     retval = {}
    #     entity_type = self._field_name_to_object[self.entity_type_field].decode(datum[self.entity_type_field])
    #     for k, v in datum.items():
    #         if k in self.entity_relations(entity_type):
    #             retval[k] = self._field_name_to_object[self.id_field_name].decode(v)
    #         elif k not in self._field_name_to_object:
    #             retval[k] = v
    #         else:
    #             try:
    #                 retval[k] = self._field_name_to_object[k].decode(v)
    #             except:
    #                 raise Exception("Could not decode {} value '{}' (spec={})".format(k, v, self._field_name_to_object[k]))
    #     return retval

    # def decode_batch(self, batch):
    #     retvals = []
    #     for i in range(len(batch[self.entity_type_field])):
    #         cur = {}
    #         for field_name, values in batch.items():
    #             if values[i] != None:
    #                 if isinstance(values[i], str):
    #                     cur[field_name] = values[i]
    #                 else:
    #                     cur[field_name] = values[i].tolist()
    #         dec = self.decode(cur)
    #         if dec[self.id_field] != None:
    #             retvals.append({k : v for k, v in dec.items() if k in list(self.entity_fields(dec[self.entity_type_field])) + [None]})
    #     return retvals

    # def encode_batch(self, batch):
    #     retval = {}
    #     fields = set()
    #     for entity in batch:
    #         for k in entity.keys():
    #             retval[k] = retval.get(k, torch.empty(size=(len(batch),)))
    #     for i, entity in enumerate(batch):
    #         for k, v in self.encode(entity).items():
    #             retval[k][i] = v
    #     return retval
    

class Dataset(object):
    """
    The Dataset class is neede mainly for operations that depend on
    graph structure, particularly those that require connected components.
    """
    def __init__(self, schema, entities):
        self.schema = schema
        print(self.schema)
        self._entities = []
        self._entity_fields = {}
        self._id_to_index = {}
        for idx, entity in enumerate(entities):
            #entity_type = entity[self._spec.entity_type_field]
            #entity_id = entity[self._spec.id_field]
            #assert (entity_id not in self._id_to_index), "The id field ('{}') must be unique".format(self._spec.id_field)
            self._id_to_index[entity[self.id_field.name]] = idx
            #self._entity_fields[entity_type] = self._spec.entity_fields(entity_type) #
            self._entities.append(entity)
        self._edges = {}
        for entity in self._entities:
            entity_type = entity[self.entity_type_field.name]
            entity_id = entity[self.id_field.name]
            source_index = self._id_to_index[entity_id]
            for relation_type in self.entity_types[entity_type].relation_fields:
                target_ids = entity.get(relation_type, [])
                for target in target_ids if isinstance(target_ids, list) else [target_ids]:
                    if target not in self._id_to_index:
                        logging.warning("Could not find target %s for entity %s relation %s", target, entity_id, relation_type)
                        continue
                    target_index = self._id_to_index[target]
                    self._edges[relation_type] = self._edges.get(relation_type, {})
                    self._edges[relation_type][source_index] = self._edges[relation_type].get(source_index, [])
                    self._edges[relation_type][source_index].append(target_index)
        self._update_components()

    @property
    def entity_types(self):
        return self.schema.entity_types
        
    @property
    def entity_type_field(self):
        return self.schema.entity_type_field

    @property
    def id_field(self):
        return self.schema.id_field        
        
    def subselect(self, indices):
        return Dataset(self._schema, [self._entities[i] for i in indices])

    def subselect_components(self, indices):
        print(self.schema)
        return Dataset(self.schema, [self._entities[j] for j in sum([self._components[i][0] for i in indices], [])])
    
    def encode(self, item):
        return self._spec.encode(item)

    def decode(self, item):
        return self._spec.decode(item)

    def _update_components(self):
        # create union adjacency matrix
        rows, cols, vals = [], [], []
        for _, rs in self._edges.items():
            for r, cs in rs.items():
                for c in cs:
                    rows.append(r)
                    cols.append(c)
                    vals.append(True)
        adjacency = scipy.sparse.csr_matrix((vals, (rows, cols)), 
                                            shape=(len(self), len(self)), 
                                            dtype=numpy.bool)

        # create list of connected components
        num, ids = connected_components(adjacency)
        components = {}    
        for i, c in enumerate(ids):
            components[c] = components.get(c, [])
            components[c].append(i)
            
        largest_component_size = 0 if len(components) == 0 else max([len(x) for x in components.values()])
        if len(components) == 0:
            raise Exception("The data is empty: this probably isn't what you want.  Perhaps add more instances, or adjust the train/dev/test split proportions?")
        logging.info("Found %d connected components with maximum size %d", len(components), largest_component_size)
        
        self._components = []
        for c in components.values():
            #component_adjacencies = {} #{k : numpy.full((len(c), len(c)), False) for k in self._edges.keys()}
            ca_rows, ca_cols = {}, {}
            g2l = {k : v for v, k in enumerate(c)}
            for gsi in c:
                lsi = g2l[gsi]
                for rel_type, rows in self._edges.items():
                    ca_rows[rel_type] = ca_rows.get(rel_type, [])
                    ca_cols[rel_type] = ca_cols.get(rel_type, [])
                    for gti in rows.get(gsi, []):                        
                        lti = g2l[gti]
                        ca_rows[rel_type].append(lsi)
                        ca_cols[rel_type].append(lti)
                        #component_adjacencies[rel_type][lsi, lti] = True
            component_adjacencies = {rel_type : scipy.sparse.csr_matrix(([True for _ in ca_rows[rel_type]], (ca_rows[rel_type], ca_cols[rel_type])), 
                                                                 shape=(len(c), len(c)), dtype=numpy.bool) for rel_type in self._edges.keys()}
            self._components.append((c, component_adjacencies)) # = [c for c in components.values()]

        
    def __getitem__(self, index):
        return self._entities[index]
    
    def __len__(self):
        return len(self._entities)

    def component(self, i):
        entity_indices, adjacencies = self._components[i]
        entities = [self[i] for i in entity_indices]
        return (entities, adjacencies)

    #@property
    #def spec(self):
    #    return self._spec
    
    #@property
    #def entity_types(self):
    #    return self.spec.entity_types
    
    #@property
    #def field_names(self):
    #    return [x for x in self._spec.keys() if isinstance(x, str)]

    @property
    def num_components(self):
        return len(self._components)

    def __str__(self):
        return "Dataset({} entities, {} components with max size {})".format(len(self),
                                                                             len(self._components),
                                                                             0 if len(self._components) == 0 else max([len(c) for c, _ in self._components]))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", help="Input file")
    parser.add_argument("--spec", dest="spec", help="Input file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    with gzip.open(args.input, "rb") as ifd:
        data = pickle.load(ifd)
        
    with gzip.open(args.spec, "rb") as ifd:
        spec = pickle.load(ifd)


