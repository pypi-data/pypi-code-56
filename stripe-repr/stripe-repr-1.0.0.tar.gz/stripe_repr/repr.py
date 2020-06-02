import datetime

import stripe


def format_stripe(obj):
    """
    Provide a more user-friendly representation of Stripe objects.

    - StripeObject is a "value object" that doesn't have its own identity.
      We provide a verbose representation of it.
    - Collection is something that has a "data" attribute.
    - Everything else usually have an ID, and can be identified as such. If possible,
      we also set the name.
    """
    if type(obj) == stripe.stripe_object.StripeObject:
        return format_value_object(obj)
    elif "data" in obj:
        return format_collection(obj)
    else:
        return format_entity(obj)


orig_repr = stripe.stripe_object.StripeObject.__repr__


def patch():
    """Patch __repr__ of Stripe objects for a more compact representation."""
    stripe.stripe_object.StripeObject.__repr__ = format_stripe


def unpatch():
    """Unpatch __repr__ of Stripe object."""
    stripe.stripe_object.StripeObject.__repr__ = orig_repr


def format_value_object(obj):
    """Helper function to format objects without IDs."""
    name = obj.__class__.__name__
    args = dict(obj).items()
    formatted_args = ", ".join(
        [
            "{}={!r}".format(k, stripe_modify_integers(v))
            for k, v in args
            if not is_empty(v)
        ]
    )
    return "{}({})".format(name, formatted_args)


def is_empty(value):
    return value is None or value == []


def format_collection(obj):
    """Helper function to format collections."""
    name = obj.__class__.__name__
    args = [
        ("data", obj.get("data")),
    ]
    formatted_args = ", ".join(
        ["{}={!r}".format(k, v) for k, v in args if v is not None]
    )
    return "{}({})".format(name, formatted_args)


def format_entity(obj):
    """Helper function to format entities (objects with IDs)."""
    name = obj.__class__.__name__
    args = [
        ("id", obj.get("id")),
        ("name", obj.get("name")),
    ]
    formatted_args = ", ".join(
        ["{}={!r}".format(k, v) for k, v in args if v is not None]
    )
    return "{}({})".format(name, formatted_args)


def stripe_modify_integers(value):
    """Helper function that formats integers as datetime objects."""
    min_ts = ts(2010, 1, 1)
    max_ts = ts(2030, 1, 1)
    if isinstance(value, int) and min_ts < value < max_ts:
        return dt(value).strftime("%FT%T")
    return value


def ts(year, month, day):
    """Return integer timestamp from a year, month and days."""
    return int(datetime.datetime(year, month, day).strftime("%s"))


def dt(timestamp):
    """Return datetime object from the timestamp."""
    return datetime.datetime.fromtimestamp(timestamp)
