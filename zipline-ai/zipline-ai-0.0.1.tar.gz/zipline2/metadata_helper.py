
import zipline2.schema.thrift.ttypes \
    as ttypes
from typing import List, Dict, Union

DATE_PARTITION_MARKER = '{{ ds }}'


def get_underlying_source(source: ttypes.Source):
    return source.entities if source.entities else source.events


def construct_dependency(table: str, query) -> Dict[str, str]:
    date_part = query.partitionColumn
    add_parts = query.additionalPartitions
    return {
        "name": f"wait_for_{table}_{(add_parts + '_') if add_parts else ''}{date_part}",
        "spec": f"{table}/{(add_parts + '/') if add_parts else ''}{date_part}={DATE_PARTITION_MARKER}",
        "start": query.startPartition,
        "end": query.endPartition
    }


def get_dependencies(source: ttypes.Source, include_mutations=False) -> List[Dict]:
    assert not include_mutations or (source.entities and source.entities.mutationTable)
    inner_source = get_underlying_source(source)
    query = inner_source.query
    base_table = source.entities.snapshotTable if source.entities else source.events.table
    dependencies = [construct_dependency(base_table, query)]
    if include_mutations:
        dependencies.append(
            construct_dependency(source.entities.mutationTable, query))
    return dependencies

