from typing import Mapping

from gql_ext.resolvers.base_resolvers import BaseMutationResolver, BaseSubscriptionResolver, BaseQueryResolver
from gql_ext.utils import import_from_module


def parse_arg(arg_value, parent, ctx):
    if not isinstance(arg_value, str):
        return arg_value
    if arg_value.startswith('parent.'):
        return parent.get(arg_value.split('.')[-1])
    if arg_value.startswith('request.'):
        return ctx['request'].get(arg_value.split('.')[-1])
    return arg_value


def parse_args(arg_value, parent, ctx):
    if isinstance(arg_value, (list, tuple)):
        return [parse_arg(arg, parent, ctx) for arg in arg_value if arg is not None]
    return parse_arg(arg_value, parent, ctx)


def init_loader(args_, loader):
    async def loader_(_item, parent, args, ctx, info):
        if args_ is not None:
            for arg_name, arg_val in args_.items():
                args[arg_name] = parse_args(arg_val, parent, ctx)
        return await loader(_item, parent, args, ctx, info)

    return loader_


def create_resolver(resolver_name: str = None, loader: str = None, endpoint: str = None,
                    batch: bool = False, args: Mapping = None, **kwargs):
    if resolver_name.startswith('Mutation.'):
        base = BaseMutationResolver
    elif resolver_name.startswith('Subscription.'):
        base = BaseSubscriptionResolver
    else:
        base = BaseQueryResolver

    loader = import_from_module(loader) if loader else base.load

    if not resolver_name.startswith('Subscription.'):  # todo to decorators
        loader = init_loader(args, loader)

    attrs = {'batch': batch,
             'endpoint': endpoint,
             'load': loader}

    return type(resolver_name, (base,), attrs)
