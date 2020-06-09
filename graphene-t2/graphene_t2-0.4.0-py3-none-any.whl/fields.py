import ast

import graphene


class ModelID(graphene.ID):
    parse_value = int
