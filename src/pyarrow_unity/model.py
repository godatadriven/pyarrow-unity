import json
from typing import Literal

import pyarrow as pa

from unitycatalog.types.table_create_params import Column

UCSupportedTypeLiteral = Literal[
    "BOOLEAN",
    "BYTE",
    "SHORT",
    "INT",
    "LONG",
    "FLOAT",
    "DOUBLE",
    "DATE",
    "TIMESTAMP",
    "TIMESTAMP_NTZ",
    "STRING",
    "BINARY",
    "DECIMAL",
    "INTERVAL",
    "ARRAY",
    "STRUCT",
    "MAP",
    "CHAR",
    "NULL",
    "USER_DEFINED_TYPE",
    "TABLE_TYPE",
]

UCSupportedFormatLiteral = Literal["DELTA", "CSV", "JSON", "AVRO", "PARQUET", "ORC", "TEXT"]


def pyarrow_to_uc_type(data_type: pa.DataType) -> UCSupportedTypeLiteral:
    """Convert a PyArrow data type to a supported Unitycatalog JSON type."""
    if pa.types.is_boolean(data_type):
        return "BOOLEAN"
    elif pa.types.is_int8(data_type):
        return "BYTE"
    elif pa.types.is_int16(data_type):
        return "SHORT"
    elif pa.types.is_int32(data_type):
        return "INT"
    elif pa.types.is_int64(data_type):
        return "LONG"
    elif pa.types.is_float32(data_type):
        return "FLOAT"
    elif pa.types.is_float64(data_type):
        return "DOUBLE"
    elif pa.types.is_date32(data_type):
        return "DATE"
    elif pa.types.is_timestamp(data_type):
        return "TIMESTAMP"
    elif pa.types.is_string(data_type):
        return "STRING"
    elif pa.types.is_binary(data_type):
        return "BINARY"
    elif pa.types.is_decimal(data_type):
        return "DECIMAL"
    elif pa.types.is_duration(data_type):
        return "INTERVAL"
    elif pa.types.is_list(data_type):
        return "ARRAY"
    elif pa.types.is_struct(data_type):
        return "STRUCT"
    elif pa.types.is_map(data_type):
        return "MAP"
    elif pa.types.is_null(data_type):
        return "NULL"
    else:
        raise NotImplementedError(f"Type {data_type} not supported")

def model_unity_schema(schema: pa.Schema) -> list[Column]:
    """Convert a PyArrow schema to a list of Unitycatalog Column objects."""
    columns = []

    for i, field in enumerate(schema):
        data_type = field.type
        json_type = pyarrow_to_uc_type(data_type)

        column = Column(
            name=field.name,
            type_name=json_type,
            nullable=field.nullable,
            comment=f"Field {field.name}",  # Generic comment, modify as needed
            position=i,
            type_json=json.dumps(
                {
                    "name": field.name,
                    "type": json_type,
                    "nullable": field.nullable,
                    "metadata": field.metadata or {},
                }
            ),
            type_precision=0,
            type_scale=0,
            type_text=json_type,
        )

        # Adjust type precision and scale for decimal types
        if pa.types.is_decimal(data_type):
            column["type_precision"] = data_type.precision
            column["type_scale"] = data_type.scale

        columns.append(column)

    return columns