import logging

from stix2 import Filter
from stix2.datastore import DataSource, DataSourceError
from red_raccoon.integrations.stix.data_sources import TAXIICollectionSource, CompositeDataSource

import hodgepodge.helpers
import hodgepodge.path
import red_raccoon.log as log
import red_raccoon.integrations.stix.data_sources as stix_data_sources
import red_raccoon.integrations.stix.filters as stix_filters
import red_raccoon.integrations.stix.parsers as stix_parsers

from hodgepodge.helpers import ensure_type

logger = logging.getLogger(__name__)


class StixClient:
    def __init__(self, data_source, ignore_revoked=True):
        self.data_source = ensure_type(data_source, DataSource)

        self.ignore_revoked = ensure_type(ignore_revoked, bool)

    def search_for_object(self, filters=None):
        objects = self.search_for_objects(filters)
        return next(iter(objects), None)

    def search_for_objects(self, filters=None):
        if filters:
            if isinstance(filters, Filter):
                filters = [filters]
            else:
                filters = hodgepodge.helpers.as_list(filters, Filter)
        else:
            filters = None

        return [stix_parsers.stix2_to_dict(row) for row in self._query_data_source(self.data_source, filters=filters)]

    def _query_data_source(self, data_source, filters=None):
        data_source_type = type(data_source).__name__

        hint = self._get_query_hint(filters)
        log.debug(logger, "Searching for objects via %s", data_source_type, hint=hint)
        try:
            objects = data_source.query(filters)
        except DataSourceError as exception:
            if isinstance(data_source, CompositeDataSource) is False:
                log.debug(logger, "Failed to read from %s: '%s'", data_source_type, exception, hint=hint)
                objects = []
            else:
                log.debug(logger, "Failed to read from %s - sequentially reading from %d data sources: '%s'",
                          data_source_type, len(data_source.data_sources), exception, hint=hint)

                objects_by_id = {}
                for data_source in data_source.get_all_data_sources():
                    for obj in self._query_data_source(data_source, filters):
                        objects_by_id[obj['id']] = obj

                objects = list(objects_by_id.values())
        else:
            log.debug(logger, "Read %d objects from %s", len(objects), data_source_type, hint=hint)

        return objects

    def _get_query_hint(self, filters=None):
        if filters:
            hint = log.get_hint(
                filters=stix_filters.get_list_of_human_readable_filters(filters),
                properties=stix_filters.get_list_of_properties_from_filters(filters)
            )
        else:
            hint = None
        return hint

    def get_object(self, object_internal_id=None, object_external_id=None, object_types=None,
                   object_names=None):

        object_internal_id = ensure_type(object_internal_id, [str, None])
        object_external_id = ensure_type(object_external_id, [str, None])
        object_types = hodgepodge.helpers.as_set(object_types, str)
        object_names = hodgepodge.helpers.as_set(object_names, str)

        hint = log.get_hint(
            object_internal_id=object_internal_id,
            object_external_id=object_external_id,
            object_types=object_types,
            object_names=object_names,
        )
        log.debug(logger, "Looking up object", hint=hint)

        if object_internal_id:
            data = self._get_object_by_internal_id(object_internal_id)
        else:
            data = self._get_object_via_search(
                object_external_id=object_external_id,
                object_types=object_types,
                object_names=object_names,
            )

        if data:
            log.debug(logger, "Found matching %s object: %s", data['type'], data['id'], hint=hint)
        else:
            log.debug(logger, "No matching object found", hint=hint)

        return data

    def _get_object_by_internal_id(self, object_internal_id):
        data = self.data_source.get(object_internal_id)
        if data:
            data = stix_parsers.stix2_to_dict(data)
        return data

    def _get_object_via_search(self, object_external_id, object_types, object_names):
        objects = self.get_objects(
            object_external_ids=hodgepodge.helpers.as_list(object_external_id, str),
            object_types=hodgepodge.helpers.as_list(object_types, str),
            object_names=hodgepodge.helpers.as_list(object_names, str),
        )
        if self.ignore_revoked:
            data = next(filter(lambda obj: not obj.get('revoked', False), objects))
        else:
            data = next(iter(objects), None)
        return data

    def get_objects(self, object_internal_ids=None, object_external_ids=None, object_types=None, object_names=None):
        object_internal_ids = hodgepodge.helpers.as_set(object_internal_ids, str)
        object_external_ids = hodgepodge.helpers.as_set(object_external_ids, str)
        object_types = hodgepodge.helpers.as_set(object_types, str)
        object_names = hodgepodge.helpers.as_set(object_names, str)

        hint = log.get_hint(
            object_internal_ids=object_internal_ids,
            object_external_ids=object_external_ids,
            object_types=object_types,
            object_names=object_names,
        )
        log.debug(logger, "Looking up objects", hint=hint)

        objects = list(self._iter_objects(
            object_internal_ids=object_internal_ids,
            object_external_ids=object_external_ids,
            object_types=object_types,
            object_names=object_names,
        ))
        if objects:
            log.debug(logger, "Found %d matching objects", len(objects), hint=hint)
        else:
            log.debug(logger, "No matching objects found", hint=hint)
        return objects

    def _iter_objects(self, object_internal_ids, object_external_ids, object_types, object_names):
        filters = stix_filters.get_filters_for_objects(
            object_internal_ids=object_internal_ids,
            object_external_ids=object_external_ids,
            object_types=object_types,
        )
        if not isinstance(self.data_source, TAXIICollectionSource):
            objects = self.search_for_objects(filters=filters)
        else:
            try:
                objects = self.search_for_objects(filters=filters)
            except UnboundLocalError:
                hint = log.get_hint(
                    object_internal_ids=object_internal_ids,
                    object_external_ids=object_external_ids,
                    object_types=object_types,
                )
                log.warning(logger, "Encountered UnboundLocalError while searching for objects - performing "
                                    "client-side filtering", hint=hint)

                objects = self.get_objects(object_types=object_types)

        for obj in objects:

            #: Filter revoked objects.
            if self.ignore_revoked and obj.get('revoked', False):
                continue

            #: Filter objects by type.
            if object_types and obj['type'] not in object_types:
                continue

            #: Filter objects by internal ID.
            if object_internal_ids and obj['id'] not in object_internal_ids:
                continue

            #: Filter objects by external ID.
            if object_external_ids and not stix_filters.object_has_matching_external_id(obj, object_external_ids):
                continue

            #: Filter objects by [name|alias].
            if object_names and not stix_filters.object_has_matching_name(obj, object_names):
                continue

            yield obj

    def get_object_internal_ids(self, object_internal_ids=None, object_external_ids=None, object_types=None,
                                object_names=None):

        if (not object_internal_ids) or (object_names or object_external_ids):
            objects = self.get_objects(
                object_internal_ids=object_internal_ids,
                object_external_ids=object_external_ids,
                object_types=object_types,
                object_names=object_names,
            )
            object_internal_ids = [obj['id'] for obj in objects]

        elif object_types:
            object_types = hodgepodge.helpers.as_set(object_types, str)
            object_internal_ids = [
                _id for _id in object_internal_ids if stix_parsers.get_type_from_internal_id(_id) in object_types
            ]
        return object_internal_ids

    def get_object_external_ids(self, object_internal_ids=None, object_external_ids=None, object_types=None,
                                object_names=None, source_names=None):

        source_names = hodgepodge.helpers.as_set(source_names, str)
        objects = self.get_objects(
            object_internal_ids=object_internal_ids,
            object_external_ids=object_external_ids,
            object_types=object_types,
            object_names=object_names,
        )
        external_ids = []
        for obj in objects:
            for external_reference in obj.get('external_references', []):
                external_id = external_reference.get('external_id')
                if not external_id:
                    continue

                #: Ignore duplicate external IDs.
                if external_id in external_ids:
                    continue

                #: Filter the stream of external IDs by source name (e.g. 'mitre-pre-attack').
                if source_names:
                    source_name = external_reference.get('source_name')
                    if not hodgepodge.helpers.string_matches_any_pattern(source_name, source_names):
                        continue

                external_ids.append(external_id)
        return hodgepodge.helpers.as_unique_list(external_ids)

    def get_relationships(self, source_object_types=None, relationship_types=None, target_object_types=None,
                          source_object_internal_ids=None, target_object_internal_ids=None):

        source_object_internal_ids = hodgepodge.helpers.as_set(source_object_internal_ids, str)
        source_object_types = hodgepodge.helpers.as_set(source_object_types, str)
        relationship_types = hodgepodge.helpers.as_set(relationship_types, str)
        target_object_internal_ids = hodgepodge.helpers.as_set(target_object_internal_ids, str)
        target_object_types = hodgepodge.helpers.as_set(target_object_types, str)

        hint = log.get_hint(
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_types=target_object_types,
            source_object_internal_ids=source_object_internal_ids,
            target_object_internal_ids=target_object_internal_ids,
        )
        log.debug(logger, "Looking up relationships", hint=hint)

        relationships = list(self._iter_relationships(
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_types=target_object_types,
            source_object_internal_ids=source_object_internal_ids,
            target_object_internal_ids=target_object_internal_ids,
        ))
        if relationships:
            source_object_internal_ids = {relationship['source_ref'] for relationship in relationships}
            source_object_types = sorted(set(map(stix_parsers.get_type_from_internal_id, source_object_internal_ids)))

            target_object_internal_ids = {relationship['target_ref'] for relationship in relationships}
            target_object_types = sorted(set(map(stix_parsers.get_type_from_internal_id, target_object_internal_ids)))

            log.debug(logger, "Found %d relationships between %d %s objects and %d %s objects",
                      len(relationships),
                      len(source_object_internal_ids), '|'.join(source_object_types),
                      len(target_object_internal_ids), '|'.join(target_object_types), hint=hint)
        else:
            log.debug(logger, "No matching relationships found", hint=hint)
        return relationships

    def _iter_relationships(self, source_object_internal_ids, source_object_types, target_object_internal_ids,
                            target_object_types, relationship_types):

        filters = stix_filters.get_filters_for_relationships(
            source_object_internal_ids=source_object_internal_ids,
            target_object_internal_ids=target_object_internal_ids,
            relationship_types=relationship_types,
        )
        for relationship in self.search_for_objects(filters=filters):

            #: Filter relationships based on whether or not they've been revoked.
            revoked = relationship.get('revoked', False)
            if revoked:
                continue

            #: Filter relationships by source object type.
            if source_object_types:
                src_type = stix_parsers.get_type_from_internal_id(relationship['source_ref'])
                if src_type not in source_object_types:
                    continue

            #: Filter relationships by target object type.
            if target_object_types:
                dst_type = stix_parsers.get_type_from_internal_id(relationship['target_ref'])
                if dst_type not in target_object_types:
                    continue

            yield relationship


class CompositeStixClient(StixClient):
    def __init__(self, data_sources, ignore_revoked=True):
        data_source = stix_data_sources.get_composite_data_source(data_sources)

        super(CompositeStixClient, self).__init__(data_source=data_source, ignore_revoked=ignore_revoked)


def get_stix_client(data=None, url=None, path=None, ignore_revoked=True):
    data_source = stix_data_sources.get_data_source(
        data=data,
        url=url,
        path=path,
    )
    return StixClient(data_source, ignore_revoked=ignore_revoked)


def get_composite_stix_client(data_sources, ignore_revoked=True):
    data_sources = hodgepodge.helpers.as_list(data_sources, (DataSource, StixClient))
    data_sources = [src.data_source if isinstance(src, StixClient) else src for src in data_sources]
    return CompositeStixClient(data_sources=data_sources, ignore_revoked=ignore_revoked)
