from stix2 import MemorySource, TAXIICollectionSource, CompositeDataSource
from stix2.datastore import DataSource
from taxii2client.v20 import Collection

from hodgepodge.helpers import ensure_type

import red_raccoon.log as log
import hodgepodge.compression
import requests.exceptions
import hodgepodge.helpers
import hodgepodge.path
import logging
import zlib
import json
import os

logger = logging.getLogger(__name__)


def get_data_source(data=None, url=None, path=None):
    if path:
        path = hodgepodge.path.realpath(path)

    hint = log.get_hint(
        data=data,
        url=url,
        path=path,
    )
    log.info(logger, "Selecting preferred STIX data source", hint=hint)

    #: STIX 2.0 collections provided as an array of dictionaries.
    if data:
        return get_memory_source(data=data)

    #: STIX 2.0 collections residing on a locally accessible filesystem.
    if path:
        if os.path.exists(path):
            return get_memory_source_from_file(path)
        else:
            logger.warning("A path was provided, but it does not exist: %s", path)

    #: STIX 2.0 collections residing on an unauthenticated TAXII 2.0 server.
    if url:
        return get_taxii_collection_source(url)

    raise ValueError("No matching STIX data source found ({})".format(hint))


def get_composite_data_source(data_sources):
    data_sources = hodgepodge.helpers.as_list(data_sources, expected_types=[DataSource])
    if len(data_sources) < 2:
        raise ValueError("At least two data sources are required - got: {}".format(
            len(data_sources)
        ))

    data_source = CompositeDataSource()
    data_source.add_data_sources(data_sources)
    return data_source


def get_taxii_collection_source(url):
    url = ensure_type(url, str)
    data_source = None

    log.debug(logger, "Attempting to access TAXII data source: %s", url)
    try:
        collection = Collection(url)
        data_source = TAXIICollectionSource(collection)
    except requests.exceptions.ConnectionError as exception:
        log.error(logger, "Failed to access TAXII data source: %s: %s", url, exception)
    else:
        hint = log.get_hint(
            collection_name=collection.title,
            collection_description=collection.description
        )
        log.info(logger, "Successfully accessed TAXII data source: %s", url, hint=hint)
    return data_source


def get_memory_source_from_file(path):
    path = hodgepodge.path.realpath(path)
    log.debug(logger, "Attempting to access filesystem data source: %s", path)
    with open(path, 'rb') as fp:
        log.info(logger, "Loading data into memory from filesystem data source: %s", path)
        data = fp.read()
        try:
            data = hodgepodge.compression.decompress_gzip(data)
        except zlib.error:
            pass

    data = json.loads(data)
    data_source = get_memory_source(data)
    return data_source


def get_memory_source(data):
    return MemorySource(stix_data=data)


def get_collection_names_from_data_source(data_source):
    if isinstance(data_source, CompositeDataSource):
        collections = sorted({data_source.collection.title for data_source in data_source.get_all_data_sources()})
    else:
        collections = [data_source.collection.title]
    return collections
