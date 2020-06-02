import datetime

from stripe import ListObject
from stripe.stripe_object import StripeObject


def format_stripe(obj):
    """
    Provide a more user-friendly representation of Stripe objects.

    - StripeObject is a "value object" that doesn't have its own identity.
      We provide a verbose representation of it.
    - Collection is something that has a "data" attribute.
    - Everything else usually have an ID, and can be identified as such. If possible,
      we also set the name.
    """
    if type(obj) == StripeObject:
        return format_value_object(obj)
    elif type(obj) == ListObject:
        return format_collection(obj)
    else:
        return format_entity(obj)


orig_repr = StripeObject.__repr__


def patch():
    """Patch __repr__ of Stripe objects for a more compact representation."""
    StripeObject.__repr__ = format_stripe
    StripeObject.formatted_dict = formatted_dict
    StripeObject.d = formatted_dict


def unpatch():
    """Unpatch __repr__ of Stripe object."""
    StripeObject.__repr__ = orig_repr
    try:
        delattr(StripeObject, "formatted_dict")
        delattr(StripeObject, "d")
    except AttributeError:
        pass


def format_value_object(obj):
    """Helper function to format objects without IDs."""
    name = obj.__class__.__name__
    compact_obj = formatted_dict(obj)
    formatted_args = ", ".join(["{}={!r}".format(k, v) for k, v in compact_obj.items()])
    return "{}({})".format(name, formatted_args)


def is_empty(value):
    return value is None or value == []


def format_collection(obj):
    """Helper function to format collections."""
    name = obj.__class__.__name__
    data = obj.get("data")
    return "{}(data={})".format(name, data)


def format_entity(obj):
    """Helper function to format entities (objects with IDs)."""
    name = obj.__class__.__name__
    args = [
        ("id", obj.get("id")),
        ("name", obj.get("name")),
        ("name", obj.get("description")),
    ]
    formatted_args = ", ".join(
        ["{}={!r}".format(k, v) for k, v in args if v is not None]
    )
    return "{}({})".format(name, formatted_args)


def formatted_dict(obj):
    """
    Helper function to provide a readabale dict.

    The function replaces integers that look like timestamps, with the real timestamp
    objects. Also, it doesn't records with None and [] to the output.
    """
    return {k: guess_datetimes(v) for k, v in dict(obj).items() if not is_empty(v)}


def guess_datetimes(value):
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
