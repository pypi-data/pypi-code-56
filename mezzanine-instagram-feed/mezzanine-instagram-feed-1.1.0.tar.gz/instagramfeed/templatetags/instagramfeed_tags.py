from __future__ import absolute_import, unicode_literals

import json
import logging
import re
import requests

from django import template
from django.core.cache import cache

from mezzanine.conf import settings

logger = logging.getLogger(__name__)
register = template.Library()

# Captures the value of the "sharedData" JS variable until the closing </script>
DATA_REGEX = re.compile(r"sharedData\s*=\s*(.*)\</script\>")


def _get_instagram_posts(username):
    """
    Get the latests posts on username's Instagram profile.

    Yep, this is just a hack that will fetch the page from Instagram
    and try to extract and parse the JSON data in the page.

    If parsed successfully, you can expect a list of Post dicts.
    Some notable keys on each dict are:

    shortcode: Unique post ID, can be used to generate permalinks
    thumbnail_src: Thumbnail path, can go directly in an <img>
    edge_media_to_caption/edges/0/node/text: Post caption as set by the user
    """
    url = "https://www.instagram.com/{}/".format(username)

    # Use ScraperAPI if the key is provided in settings
    if getattr(settings, "SCRAPERAPI_KEY", None):
        key = settings.SCRAPERAPI_KEY
        url = "http://api.scraperapi.com/?api_key={}&url={}".format(key, url)

    response = requests.get(url)
    if response.status_code != 200:
        logger.error(
            "Failed to get data for {} ({}) {}".format(
                username, response.status_code, response.text
            )
        )
        return []

    match = DATA_REGEX.search(response.text)
    try:
        data = json.loads(match.group(1).strip().rstrip(";"))
        data = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        data = data["edge_owner_to_timeline_media"]["edges"]
        return [d["node"] for d in data]
    except (KeyError, AttributeError, ValueError):
        logger.exception("Could not read profile data for {}".format(username))
        return []


@register.simple_tag
def instagram_posts(username, limit=12):
    """
    Put a list of Instagram posts into the template context.
    """
    CACHE_KEY = "instagram_%s" % username
    posts = cache.get(CACHE_KEY)

    # Serve from cache if available
    if posts is not None:
        return posts[:limit]

    # Else, fetch and store in cache
    posts = _get_instagram_posts(username)
    cache.set(CACHE_KEY, posts, 60 * 60 * 8)  # 8 hours
    return posts[:limit]
