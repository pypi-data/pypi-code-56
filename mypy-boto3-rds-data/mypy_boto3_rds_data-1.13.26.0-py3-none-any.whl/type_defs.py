"""
Main interface for rds-data service type definitions.

Usage::

    ```python
    from mypy_boto3_rds_data.type_defs import ArrayValueTypeDef

    data: ArrayValueTypeDef = {...}
    ```
"""
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ArrayValueTypeDef",
    "ColumnMetadataTypeDef",
    "FieldTypeDef",
    "RecordTypeDef",
    "ResultFrameTypeDef",
    "ResultSetMetadataTypeDef",
    "SqlStatementResultTypeDef",
    "StructValueTypeDef",
    "UpdateResultTypeDef",
    "ValueTypeDef",
    "BatchExecuteStatementResponseTypeDef",
    "BeginTransactionResponseTypeDef",
    "CommitTransactionResponseTypeDef",
    "ExecuteSqlResponseTypeDef",
    "ExecuteStatementResponseTypeDef",
    "ResultSetOptionsTypeDef",
    "RollbackTransactionResponseTypeDef",
    "SqlParameterTypeDef",
)

ArrayValueTypeDef = TypedDict(
    "ArrayValueTypeDef",
    {
        "arrayValues": List["ArrayValueTypeDef"],
        "booleanValues": List[bool],
        "doubleValues": List[float],
        "longValues": List[int],
        "stringValues": List[str],
    },
    total=False,
)

ColumnMetadataTypeDef = TypedDict(
    "ColumnMetadataTypeDef",
    {
        "arrayBaseColumnType": int,
        "isAutoIncrement": bool,
        "isCaseSensitive": bool,
        "isCurrency": bool,
        "isSigned": bool,
        "label": str,
        "name": str,
        "nullable": int,
        "precision": int,
        "scale": int,
        "schemaName": str,
        "tableName": str,
        "type": int,
        "typeName": str,
    },
    total=False,
)

FieldTypeDef = TypedDict(
    "FieldTypeDef",
    {
        "arrayValue": "ArrayValueTypeDef",
        "blobValue": bytes,
        "booleanValue": bool,
        "doubleValue": float,
        "isNull": bool,
        "longValue": int,
        "stringValue": str,
    },
    total=False,
)

RecordTypeDef = TypedDict("RecordTypeDef", {"values": List["ValueTypeDef"]}, total=False)

ResultFrameTypeDef = TypedDict(
    "ResultFrameTypeDef",
    {"records": List["RecordTypeDef"], "resultSetMetadata": "ResultSetMetadataTypeDef"},
    total=False,
)

ResultSetMetadataTypeDef = TypedDict(
    "ResultSetMetadataTypeDef",
    {"columnCount": int, "columnMetadata": List["ColumnMetadataTypeDef"]},
    total=False,
)

SqlStatementResultTypeDef = TypedDict(
    "SqlStatementResultTypeDef",
    {"numberOfRecordsUpdated": int, "resultFrame": "ResultFrameTypeDef"},
    total=False,
)

StructValueTypeDef = TypedDict(
    "StructValueTypeDef", {"attributes": List["ValueTypeDef"]}, total=False
)

UpdateResultTypeDef = TypedDict(
    "UpdateResultTypeDef", {"generatedFields": List["FieldTypeDef"]}, total=False
)

ValueTypeDef = TypedDict(
    "ValueTypeDef",
    {
        "arrayValues": List["ValueTypeDef"],
        "bigIntValue": int,
        "bitValue": bool,
        "blobValue": bytes,
        "doubleValue": float,
        "intValue": int,
        "isNull": bool,
        "realValue": float,
        "stringValue": str,
        "structValue": "StructValueTypeDef",
    },
    total=False,
)

BatchExecuteStatementResponseTypeDef = TypedDict(
    "BatchExecuteStatementResponseTypeDef",
    {"updateResults": List["UpdateResultTypeDef"]},
    total=False,
)

BeginTransactionResponseTypeDef = TypedDict(
    "BeginTransactionResponseTypeDef", {"transactionId": str}, total=False
)

CommitTransactionResponseTypeDef = TypedDict(
    "CommitTransactionResponseTypeDef", {"transactionStatus": str}, total=False
)

ExecuteSqlResponseTypeDef = TypedDict(
    "ExecuteSqlResponseTypeDef",
    {"sqlStatementResults": List["SqlStatementResultTypeDef"]},
    total=False,
)

ExecuteStatementResponseTypeDef = TypedDict(
    "ExecuteStatementResponseTypeDef",
    {
        "columnMetadata": List["ColumnMetadataTypeDef"],
        "generatedFields": List["FieldTypeDef"],
        "numberOfRecordsUpdated": int,
        "records": List[List["FieldTypeDef"]],
    },
    total=False,
)

ResultSetOptionsTypeDef = TypedDict(
    "ResultSetOptionsTypeDef",
    {"decimalReturnType": Literal["DOUBLE_OR_LONG", "STRING"]},
    total=False,
)

RollbackTransactionResponseTypeDef = TypedDict(
    "RollbackTransactionResponseTypeDef", {"transactionStatus": str}, total=False
)

SqlParameterTypeDef = TypedDict(
    "SqlParameterTypeDef",
    {
        "name": str,
        "typeHint": Literal["DATE", "DECIMAL", "TIME", "TIMESTAMP"],
        "value": "FieldTypeDef",
    },
    total=False,
)
