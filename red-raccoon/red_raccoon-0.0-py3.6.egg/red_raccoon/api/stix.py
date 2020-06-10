"""
The following module contains functionality for working with different STIX 2.x collections.
"""
import logging
import os

import stix2.utils
import requests.exceptions

from stix2 import TAXIICollectionSource, MemorySource, CompositeDataSource, Filter
from stix2.datastore import DataSource
from taxii2client import Collection

import hodgepodge.helpers
import hodgepodge.path
import red_raccoon.stix.filters
import red_raccoon.stix.parsers

from hodgepodge.helpers import ensure_type

logger = logging.getLogger(__name__)


class StixClient:
    def __init__(self, data_source, tags=None):
        self.data_source = ensure_type(data_source, DataSource)
        self.tags = hodgepodge.helpers.as_unique_list(tags, str)

    def search_for_objects(self, filters=None):
        """
        Searches for STIX 2.x objects which map the provided sequence of filters (if applicable).

        :param filters: an optional sequence of STIX 2.x filters.
        :return: an iterator of STIX 2.x objects.
        """
        if isinstance(filters, Filter):
            filters = [filters]
        else:
            filters = hodgepodge.helpers.as_list(filters, Filter)

        tags = self.tags or None
        if not filters:
            logger.info("Searching for all objects (tags: {%s)", tags)
        else:
            object_type_filter = red_raccoon.stix.filters.select_object_type_filter(filters)
            if not object_type_filter:
                logger.info("Searching for all objects matching %d filters (tags: %s)",
                            len(filters), tags)
            else:
                types = hodgepodge.helpers.as_set(object_type_filter.value)
                logger.info(
                    "Searching for %s objects matching %d filters (%s) (tags: %s)",
                    '|'.join(types), len(filters),
                    ', '.join(('{} {} {}'.format(f.property, f.op, f.value) for f in filters)),
                    tags,
                )

        #: Search for those objects.
        return self._query(filters)

    def search_for_object(self, filters=None):
        """
        Searches for the first STIX 2.x object which matches the provided sequence of filters.

        :param filters: an optional sequence of filters.
        :return: the first matching STIX 2.x object.
        """
        return next(iter(self.search_for_objects(filters=filters)), None)

    def _query(self, filters=None):
        try:
            stream = self.data_source.query(filters)
        except stix2.datastore.DataSourceError as exception:
            logger.error("Failed to read from %s: %s (tags: %s)",
                         type(self.data_source).__name__, exception, self.tags or None)
        else:
            for row in stream:
                yield row

    def get_object_by_name(self, object_names=None, object_types=None):
        """
        Searches for objects by name, or alias (e.g. "FIN*" for all financially-motivated threat
        actors, or "APT28" as an example of how to search for a specific threat actor by alias).

        :param object_names: an optional sequence of object names (e.g. "APT28" or "FIN*").
        :param object_types: an optional sequence of object types (e.g. "attack-pattern").
        :return: a single STIX 2.x object.
        """
        names = hodgepodge.helpers.as_set(object_names, str)
        types = hodgepodge.helpers.as_set(object_types, str)
        tags = self.tags or None

        if types:
            logger.info("Looking up %s object by name: %s (tags: %s)",
                        '|'.join(types), ', '.join(names), tags)
        else:
            logger.info("Looking up object by name: %s (tags: %s)", ', '.join(names), tags)

        return next(self.iter_objects(object_names=object_names, object_types=object_types), None)

    def get_object_by_id(self, object_id, object_types=None):
        """
        Searches for objects by internal or external ID.

        :param object_id: an internal or external ID.
        :param object_types: an optional sequence of object types (e.g. "attack-pattern").
        :return: a single STIX 2.x object.
        """
        object_id = ensure_type(object_id, str)

        #: If the provided ID was an internal ID.
        if red_raccoon.stix.parsers.is_id(object_id):
            obj = self.get_object_by_internal_id(object_id)
        else:
            obj = self.get_object_by_external_id(object_id, object_types)
        return obj

    def get_object_by_internal_id(self, object_internal_id):
        """
        Searches for objects by internal ID.

        :param object_internal_id: an internal ID.
        :return: a single STIX 2.x object.
        """
        object_internal_id = ensure_type(object_internal_id, str)
        tags = self.tags or None

        logger.info("Looking up object by internal ID: %s (tags: %s)", object_internal_id, tags)
        return self.data_source.get(object_internal_id)

    def get_object_by_external_id(self, object_external_id, object_types=None):
        """
        Searches for objects by external ID.

        :param object_external_id: an external ID.
        :param object_types: an optional sequence of object types.
        :return: a single STIX 2.x object.
        """
        object_external_id = ensure_type(object_external_id, str)
        tags = self.tags or None

        logger.info("Looking up object by external ID: %s (tags: %s)", object_external_id, tags)
        filters = red_raccoon.stix.filters.get_filters_for_objects(
            object_external_ids=[object_external_id],
            object_types=object_types,
        )
        return self.search_for_object(filters)

    def get_objects(self, object_ids=None, object_names=None, object_types=None):
        """
        Searches for STIX 2.x objects.

        :param object_ids: an optional sequence of internal IDs, or external IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: a list of STIX 2.x objects.
        """
        return list(self.iter_objects(
            object_ids=object_ids,
            object_names=object_names,
            object_types=object_types,
        ))

    def get_objects_by_internal_id(self, object_internal_ids=None, object_names=None,
                                   object_types=None):
        """
        Searches for STIX 2.x objects.

        :param object_internal_ids: an optional sequence of internal IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: a list of STIX 2.x objects.
        """
        return list(self.iter_objects_by_internal_id(
            object_internal_ids=object_internal_ids,
            object_names=object_names,
            object_types=object_types,
        ))

    def get_objects_by_external_id(self, object_external_ids=None, object_names=None,
                                   object_types=None):
        """
        Searches for STIX 2.x objects.

        :param object_external_ids: an optional sequence of external IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: a list of STIX 2.x objects.
        """
        return list(self.iter_objects_by_external_id(
            object_external_ids=object_external_ids,
            object_names=object_names,
            object_types=object_types,
        ))

    def iter_objects(self, object_ids=None, object_names=None, object_types=None):
        """
        Searches for STIX 2.x objects.

        :param object_ids: an optional sequence of internal IDs, or external IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: an iterator of STIX 2.x objects.
        """
        if object_ids:
            object_internal_ids, object_external_ids = partition_object_ids(object_ids)
            filters = red_raccoon.stix.filters.get_filters_for_objects(
                object_internal_ids=object_internal_ids,
                object_external_ids=object_external_ids,
                object_types=object_types,
            )
        else:
            filters = red_raccoon.stix.filters.get_filters_for_objects(object_types=object_types)

        #: Search for objects, and optionally filter by name.
        stream = self.search_for_objects(filters)
        if object_names:
            stream = filter_objects_by_name(stream, object_names)
        return stream

    def iter_objects_by_internal_id(self, object_internal_ids, object_names=None,
                                    object_types=None):
        """
        Searches for STIX 2.x objects.

        :param object_internal_ids: an optional sequence of internal IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: a list of STIX 2.x objects.
        """
        filters = red_raccoon.stix.filters.get_filters_for_objects(
            object_internal_ids=object_internal_ids,
            object_types=object_types,
        )
        stream = self.search_for_objects(filters)
        if object_names:
            stream = filter_objects_by_name(stream, object_names)
        return stream

    def iter_objects_by_external_id(self, object_external_ids, object_names=None,
                                    object_types=None):
        """
        Searches for STIX 2.x objects.

        :param object_external_ids: an optional sequence of external IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: a list of STIX 2.x objects.
        """
        filters = red_raccoon.stix.filters.get_filters_for_objects(
            object_external_ids=object_external_ids,
            object_types=object_types,
        )
        stream = self.search_for_objects(filters)
        if object_names:
            stream = filter_objects_by_name(stream, object_names)
        return stream

    def get_object_internal_ids(self, object_ids=None, object_names=None, object_types=None):
        """
        Looks up the internal ID associated with the specified STIX 2.x objects.

        :param object_ids: an optional sequence of internal IDs, or external IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: a list of STIX 2.x objects.
        """
        return list(self.iter_object_internal_ids(
            object_ids=object_ids,
            object_names=object_names,
            object_types=object_types,
        ))

    def iter_object_internal_ids(self, object_ids=None, object_names=None, object_types=None):
        """
        Looks up the internal ID associated with the specified STIX 2.x objects.

        :param object_ids: an optional sequence of internal IDs, or external IDs.
        :param object_names: an optional sequence of object names.
        :param object_types: an optional sequence of object types.
        :return: a list of STIX 2.x objects.
        """
        objects = self.iter_objects(
            object_ids=object_ids,
            object_names=object_names,
            object_types=object_types
        )
        for obj in objects:
            yield obj.id

    def get_directed_relationships(self, source_object_internal_ids=None, source_object_types=None,
                                   target_object_internal_ids=None, target_object_types=None,
                                   relationship_types=None):
        """
        Looks up the directed relationships that exist between STIX 2.x objects.

        :param source_object_internal_ids: an optional sequence of source object internal IDs.
        :param source_object_types: an optional sequence of source object types.
        :param target_object_internal_ids: an optional sequence of target object internal IDs.
        :param target_object_types: an optional sequence of target object types.
        :param relationship_types: an optional sequence of relationship types.
        :return: a list of relationships.
        """
        relationships = self.iter_directed_relationships(
            source_object_internal_ids=source_object_internal_ids,
            source_object_types=source_object_types,
            target_object_internal_ids=target_object_internal_ids,
            target_object_types=target_object_types,
            relationship_types=relationship_types
        )
        return list(relationships)

    def iter_directed_relationships(self, source_object_internal_ids=None, source_object_types=None,
                                    target_object_internal_ids=None, target_object_types=None,
                                    relationship_types=None):
        """
        Looks up the directed relationships that exist between STIX 2.x objects.

        :param source_object_internal_ids: an optional sequence of source object internal IDs.
        :param source_object_types: an optional sequence of source object types.
        :param target_object_internal_ids: an optional sequence of target object internal IDs.
        :param target_object_types: an optional sequence of target object types.
        :param relationship_types: an optional sequence of relationship types.
        :return: an iterator of relationships.
        """
        #: Normalize the provided set(s) of object types.
        source_object_types = hodgepodge.helpers.as_set(source_object_types)
        target_object_types = hodgepodge.helpers.as_set(target_object_types)

        #: Lookup relationships.
        filters = red_raccoon.stix.filters.get_filters_for_relationships(
            source_object_internal_ids=hodgepodge.helpers.as_set(source_object_internal_ids),
            target_object_internal_ids=hodgepodge.helpers.as_set(target_object_internal_ids),
            relationship_types=relationship_types,
        )
        for relationship in self.search_for_objects(filters):

            #: Optionally filter relationships by target type.
            if source_object_types:
                if get_type_from_id(relationship['source_ref']) not in source_object_types:
                    continue

            #: Optionally filter relationships by target type.
            if target_object_types:
                if get_type_from_id(relationship['target_ref']) not in target_object_types:
                    continue

            yield relationship

    def get_undirected_relationships(self, object_internal_ids=None, object_types=None,
                                     relationship_types=None):
        """
        Looks up the undirected relationships that exist between STIX 2.x objects.

        :param object_internal_ids: an optional sequence of source/target object internal IDs.
        :param object_types: an optional sequence of source/target object types.
        :param relationship_types: an optional sequence of relationship types.
        :return: a list of relationships.
        """
        relationships = self.iter_undirected_relationships(
            object_internal_ids=object_internal_ids,
            object_types=object_types,
            relationship_types=relationship_types
        )
        return list(relationships)

    def iter_undirected_relationships(self, object_internal_ids=None, object_types=None,
                                      relationship_types=None):
        """
        Looks up the undirected relationships that exist between STIX 2.x objects.

        :param object_internal_ids: an optional sequence of source/target object internal IDs.
        :param object_types: an optional sequence of source/target object types.
        :param relationship_types: an optional sequence of relationship types.
        :return: an iterator of relationships.
        """
        object_types = hodgepodge.helpers.as_set(object_types)
        object_internal_ids = hodgepodge.helpers.as_set(object_internal_ids)

        if object_internal_ids:
            streams = [
                self.iter_directed_relationships(
                    source_object_internal_ids=object_internal_ids,
                    relationship_types=relationship_types,
                ),
                self.iter_directed_relationships(
                    target_object_internal_ids=object_internal_ids,
                    relationship_types=relationship_types,
                )
            ]
        else:
            streams = [self.iter_directed_relationships(relationship_types=relationship_types)]

        for stream in streams:
            for relationship in stream:
                if object_types:
                    src_type = get_type_from_id(relationship['src'])
                    dst_type = get_type_from_id(relationship['dst'])
                    if src_type not in object_types and dst_type not in object_types:
                        continue

                yield relationship

    def get_source_object_internal_ids_by_target_objects(self, source_object_internal_ids=None,
                                                         target_object_internal_ids=None,
                                                         source_object_types=None,
                                                         target_object_types=None,
                                                         relationship_types=None):
        """
        Filters the provided sequence of source object internal IDs by the provided sequence of
        target objects internal IDs, or types.

        :param source_object_internal_ids: an optional sequence of source object internal IDs.
        :param source_object_types: an optional sequence of source object types.
        :param target_object_internal_ids: an optional sequence of target object internal IDs.
        :param target_object_types: an optional sequence of target object types.
        :param relationship_types: an optional sequence of relationship types.
        :return: an set of source object internal IDs.
        """
        #: Normalize the set of source objects.
        source_object_internal_ids = hodgepodge.helpers.as_set(source_object_internal_ids, str)
        source_object_types = hodgepodge.helpers.as_set(source_object_types, str)
        if source_object_types is None:
            source_object_types = {
                red_raccoon.stix.parsers.get_type_from_id(o) for o in source_object_internal_ids
            }

        #: Normalize the set of target objects.
        target_object_internal_ids = hodgepodge.helpers.as_set(target_object_internal_ids, str)
        target_object_types = hodgepodge.helpers.as_set(target_object_types, str)
        if target_object_types is None:
            target_object_types = {
                red_raccoon.stix.parsers.get_type_from_id(o) for o in target_object_internal_ids
            }

        #: Lookup relationships.
        relationships = self.get_directed_relationships(
            source_object_internal_ids=source_object_internal_ids,
            source_object_types=source_object_types,
            target_object_internal_ids=target_object_internal_ids,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )
        return {o.source_ref for o in relationships}

    def get_source_object_by_target_objects(self, source_object_internal_ids=None,
                                            target_object_internal_ids=None,
                                            source_object_types=None,
                                            target_object_types=None,
                                            relationship_types=None):
        """
        Filters the provided sequence of source objects by the provided sequence of target objects.

        :param source_object_internal_ids: an optional sequence of source object internal IDs.
        :param source_object_types: an optional sequence of source object types.
        :param target_object_internal_ids: an optional sequence of target object internal IDs.
        :param target_object_types: an optional sequence of target object types.
        :param relationship_types: an optional sequence of relationship types.
        :return: an set of source object internal IDs.
        """
        source_object_internal_ids = self.get_source_object_internal_ids_by_target_objects(
            source_object_internal_ids=source_object_internal_ids,
            target_object_internal_ids=target_object_internal_ids,
            source_object_types=source_object_types,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )
        return self.get_objects_by_internal_id(source_object_internal_ids)

    def get_target_object_internal_ids_by_source_objects(self, source_object_internal_ids=None,
                                                         target_object_internal_ids=None,
                                                         source_object_types=None,
                                                         target_object_types=None,
                                                         relationship_types=None):
        """
        Filters the provided sequence of target object internal IDs by the provided sequence of
        source object internal IDs, or types.

        :param source_object_internal_ids: an optional sequence of source object internal IDs.
        :param source_object_types: an optional sequence of source object types.
        :param target_object_internal_ids: an optional sequence of target object internal IDs.
        :param target_object_types: an optional sequence of target object types.
        :param relationship_types: an optional sequence of relationship types.
        :return: a set of target object internal IDs.
        """
        #: Normalize the set of source objects.
        source_object_internal_ids = hodgepodge.helpers.as_set(source_object_internal_ids, str)
        source_object_types = hodgepodge.helpers.as_set(source_object_types, str)
        if source_object_types is None:
            source_object_types = {
                red_raccoon.stix.parsers.get_type_from_id(o) for o in source_object_internal_ids
            }

        #: Normalize the set of target objects.
        target_object_internal_ids = hodgepodge.helpers.as_set(target_object_internal_ids, str)
        target_object_types = hodgepodge.helpers.as_set(target_object_types, str)
        if target_object_types is None:
            target_object_types = {
                red_raccoon.stix.parsers.get_type_from_id(o) for o in target_object_internal_ids
            }

        #: Lookup relationships.
        relationships = self.get_directed_relationships(
            source_object_internal_ids=source_object_internal_ids,
            source_object_types=source_object_types,
            target_object_internal_ids=target_object_internal_ids,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )
        return {o.target_ref for o in relationships}


def filter_objects_by_name(objects, object_names):
    """
    Filter the provided sequence of objects by name, or alias (e.g. "APT28" or "FIN*" for all
    financially motivated threat groups).

    :return: an iterator of STIX 2.x objects.
    """
    for obj in objects:
        if _object_has_matching_name(obj, object_names):
            yield obj


def _object_has_matching_name(obj, object_names):
    name = obj.get('name')
    aliases = obj.get('aliases', [])

    if not (name or aliases):
        return False

    if name and aliases:
        fields = [name] + aliases
    elif name:
        fields = [name]
    else:
        fields = aliases

    return hodgepodge.helpers.any_string_matches_any_pattern(
        strings=fields, patterns=object_names, case_sensitive=False,
    )


class TaxiiClient(StixClient):
    """"
    Reads STIX 2.x data from a remote TAXII collection.
    """
    def __init__(self, url, tags=None):
        data_source = TAXIICollectionSource(Collection(url))
        super(TaxiiClient, self).__init__(data_source=data_source, tags=tags)


class MemoryClient(StixClient):
    """"
    Reads STIX 2.x data from memory (STIX 2.x data should be provided as a list of dictionaries).
    """
    def __init__(self, data, tags=None):
        data_source = MemorySource(stix_data=data)
        super(MemoryClient, self).__init__(data_source=data_source, tags=tags)


class FilesystemClient(StixClient):
    """
    Reads STIX 2.x data from the local filesystem.
    """
    def __init__(self, path, tags=None):
        path = self._get_path(path)
        data_source = self._get_memory_source(path)

        super(FilesystemClient, self).__init__(data_source=data_source, tags=tags)

    def _get_path(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        return hodgepodge.path.realpath(path)

    def _get_memory_source(self, path):
        data_source = MemorySource()
        data_source.load_from_file(path)
        return data_source


class CompositeClient(StixClient):
    """
    A composite STIX 2.x client is capable of reading STIX 2.x data from multiple repositories (e.g.
    the MITRE ATT&CK Enterprise, Mobile, and Pre-ATT&CK matrices from an external TAXII server, and
    the MITRE CAPEC matrix via a local repository).
    """
    def __init__(self, data_sources, tags=None):
        data_source = self._parse_data_sources(data_sources)
        super(CompositeClient, self).__init__(data_source=data_source, tags=tags)

    def _query(self, filters=None):
        try:
            stream = self.data_source.query(filters)
        except stix2.datastore.DataSourceError as exception:
            data_sources = self.data_source.get_all_data_sources()
            logger.warning(
                "Failed to read from %s - reading from %d data source(s): %s (tags: %s)",
                type(self.data_source).__name__, len(data_sources), exception, self.tags or None
            )
            for data_source in data_sources:
                for row in self._query_data_source(data_source, filters):
                    yield row
        else:
            for row in stream:
                yield row

    def _query_data_source(self, data_source, filters):
        try:
            stream = data_source.query(filters)
        except stix2.datastore.DataSourceError as exception:
            logger.warning(
                "Failed to read from %s under %s: %s (tags: %s)",
                type(data_source).__name__, type(self.data_source).__name__, exception,
                self.tags or None
            )
        else:
            for row in stream:
                yield row

    def _parse_data_sources(self, data_sources):
        data_sources = list(map(self._parse_data_source, hodgepodge.helpers.as_list(data_sources)))

        #: Pack each of the provided test_data sources into a composite test_data source.
        composite_data_source = CompositeDataSource()
        composite_data_source.add_data_sources(data_sources)
        return composite_data_source

    def _parse_data_source(self, data_source):
        if isinstance(data_source, DataSource):
            return data_source

        if isinstance(data_source, StixClient):
            return data_source.data_source

        raise ValueError("Unsupported data source '{}': {}".format(type(data_source), data_source))


def get_default_client(data=None, url=None, path=None, tags=None, prefer_offline_repositories=True):
    """
    Instantiates the preferred STIX 2.x client (e.g. a client for reading data from an external
    TAXII server, or a location on the local filesystem).

    :param data: an optional sequence of STIX 2.x objects represented as dictionaries.
    :param url: an optional URL to a TAXII collection (e.g. the MITRE ATT&CK Enterprise matrix at "
        https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e").

    :param path: an optional path to a local STIX 2.x repository.
    :param tags: an optional sequence of tags to associate with the data source.
    :param prefer_offline_repositories: whether or not to prefer data from offline repositories.
    :return: a STIX 2.x client.
    """
    tags = hodgepodge.helpers.as_unique_list(tags, str) or None
    if not (data or url or path):
        raise ValueError("A path, a URL, or list of STIX 2.x objects as dicts is required")

    #: Always prefer in-memory data (STIX).
    if data:
        logger.info("Using in-memory STIX API client")
        return MemoryClient(data, tags)

    #: Determine which API client to use.
    if path:
        logger.debug("Selecting default STIX API client (url: %s, path: %s (exists: %s), tags: %s)",
                     url, path, os.path.exists(path), tags)
    else:
        logger.debug("Selecting default STIX API client (url: %s, path: %s, tags: %s",
                     url, path, tags)

    #: Always fall-back to online data (TAXII).
    if not path or os.path.exists(path) is False:
        client = red_raccoon.api.stix.get_taxii_client(url, tags)

    #: Allow the user to choose between an online, or offline repository.
    else:
        path = hodgepodge.path.realpath(path)
        if prefer_offline_repositories:
            client = get_filesystem_client(path, tags) or get_taxii_client(url, tags)
        else:
            client = get_taxii_client(url, tags) or get_filesystem_client(path, tags)

    #: If we failed to connect to all of the provided data sources, let the user know why.
    if not client:
        raise ValueError("Failed to load data (url: {}, path: {}, tags: {})".format(
            url, path, tags
        ))
    return client


def get_filesystem_client(path, tags=None):
    """
    Instantiates a STIX 2.x client which reads data from a local filesystem.

    :param path: a path to a local STIX 2.x repository.
    :param tags: an optional sequence of tags to associate with the data source.
    :return: a STIX 2.x client.
    """
    path = hodgepodge.path.realpath(ensure_type(path, str))
    tags = tags or None

    #: Attempt to read from the local filesystem.
    logger.debug("Attempting to load data from: %s (tags: %s)", path, tags)
    try:
        client = FilesystemClient(path, tags=tags)
    except FileNotFoundError as exception:
        logger.error("Failed to load data from: %s (tags: %s): %s", path, tags, exception)
    else:
        logger.info("Successfully loaded data from: %s (tags: %s)", path, tags)
        return client


def get_taxii_client(url, tags=None):
    """
    Instantiates a STIX 2.x client which reads data from a TAXII service.

    :param url: a URL to a TAXII collection (e.g. the MITRE ATT&CK Enterprise matrix at
        "https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e").

    :param tags: an optional sequence of tags to associate with the data source.
    :return: a STIX 2.x client.
    """
    url = ensure_type(url, str)
    tags = tags or None

    logger.debug("Attempting to load data from: %s (tags: %s)", url, tags)
    try:
        client = TaxiiClient(url, tags=tags)
    except requests.exceptions.ConnectionError as exception:
        logger.error("Failed to load data from: %s: %s (tags: %s)", url, exception, tags)
    else:
        logger.info("Successfully loaded data from: %s (tags: %s)", url, tags)
        return client


def get_composite_client(data_sources, tags=None):
    """
    Instantiates a composite STIX 2.x client which reads data from one, or more data sources.

    :param data_sources: a sequence of STIX 2.x data sources, or API clients.
    :param tags: an optional sequence of tags to associate with the data source.
    :return: a STIX 2.x client.
    """
    return CompositeClient(data_sources=data_sources, tags=tags)


def get_type_from_id(object_internal_id):
    """
    Parses the STIX 2.x object type from an internal ID.

    :param object_internal_id: a STIX 2.x internal ID.
    :return: an object type.
    """
    object_internal_id = ensure_type(object_internal_id, str)
    return red_raccoon.stix.parsers.get_type_from_id(object_internal_id)


def partition_object_ids(object_ids):
    """
    Partitions the provided stream of object IDs into a set of internal IDs, and a set of external
    IDs.

    :param object_ids: a set of object IDs.
    :return: a tuple of internal IDs, and external IDs.
    """
    internal_ids = set()
    external_ids = set()
    for object_id in hodgepodge.helpers.as_set(object_ids, str):
        if red_raccoon.stix.parsers.is_id(object_id):
            internal_ids.add(object_id)
        else:
            external_ids.add(object_id)
    return internal_ids, external_ids
