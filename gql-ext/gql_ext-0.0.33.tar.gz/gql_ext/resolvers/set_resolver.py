from typing import Mapping

from tartiflette import Resolver, Subscription

from .resolver_cls_creator import create_resolver


def set_resolver(resolver_name: str, schema: str, args: Mapping):
    dec_cls = Subscription if resolver_name.startswith('Subscription.') else Resolver
    dec = dec_cls(resolver_name, schema)
    resolver_cls = create_resolver(**args, resolver_name=resolver_name)

    return dec(resolver_cls().load)
