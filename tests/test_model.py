import pytest
import pyarrow as pa
from pyarrow_unity.model import pyarrow_to_uc_type, model_unity_schema

def test_pyarrow_type_to_supported_uc_json_type_boolean():
    assert pyarrow_to_uc_type(pa.bool_()) == "BOOLEAN"

def test_pyarrow_type_to_supported_uc_json_type_int8():
    assert pyarrow_to_uc_type(pa.int8()) == "BYTE"

def test_pyarrow_type_to_supported_uc_json_type_int16():
    assert pyarrow_to_uc_type(pa.int16()) == "SHORT"

def test_pyarrow_type_to_supported_uc_json_type_int32():
    assert pyarrow_to_uc_type(pa.int32()) == "INT"

def test_pyarrow_type_to_supported_uc_json_type_int64():
    assert pyarrow_to_uc_type(pa.int64()) == "LONG"

def test_pyarrow_type_to_supported_uc_json_type_float32():
    assert pyarrow_to_uc_type(pa.float32()) == "FLOAT"

def test_pyarrow_type_to_supported_uc_json_type_float64():
    assert pyarrow_to_uc_type(pa.float64()) == "DOUBLE"

def test_pyarrow_type_to_supported_uc_json_type_date32():
    assert pyarrow_to_uc_type(pa.date32()) == "DATE"

def test_pyarrow_type_to_supported_uc_json_type_timestamp():
    assert pyarrow_to_uc_type(pa.timestamp('s')) == "TIMESTAMP"

def test_pyarrow_type_to_supported_uc_json_type_string():
    assert pyarrow_to_uc_type(pa.string()) == "STRING"

def test_pyarrow_type_to_supported_uc_json_type_binary():
    assert pyarrow_to_uc_type(pa.binary()) == "BINARY"

def test_pyarrow_type_to_supported_uc_json_type_decimal():
    assert pyarrow_to_uc_type(pa.decimal128(10, 2)) == "DECIMAL"

def test_pyarrow_type_to_supported_uc_json_type_duration():
    assert pyarrow_to_uc_type(pa.duration('s')) == "INTERVAL"

def test_pyarrow_type_to_supported_uc_json_type_list():
    assert pyarrow_to_uc_type(pa.list_(pa.int32())) == "ARRAY"

def test_pyarrow_type_to_supported_uc_json_type_struct():
    assert pyarrow_to_uc_type(pa.struct([pa.field('f1', pa.int32())])) == "STRUCT"

def test_pyarrow_type_to_supported_uc_json_type_map():
    assert pyarrow_to_uc_type(pa.map_(pa.string(), pa.int32())) == "MAP"

def test_pyarrow_type_to_supported_uc_json_type_null():
    assert pyarrow_to_uc_type(pa.null()) == "NULL"

def test_pyarrow_type_to_supported_uc_json_type_not_supported():
    with pytest.raises(NotImplementedError):
        pyarrow_to_uc_type(pa.time32('s'))

def test_model_unity_schema():
    schema = pa.schema([
        pa.field('col1', pa.int32(), nullable=True),
        pa.field('col2', pa.string(), nullable=False),
        pa.field('col3', pa.decimal128(10, 2), nullable=True)
    ])
    columns = model_unity_schema(schema)
    assert len(columns) == 3
    assert columns[0]['name'] == 'col1'
    assert columns[0]['type_name'] == 'INT'
    assert columns[0]['nullable'] is True
    assert columns[1]['name'] == 'col2'
    assert columns[1]['type_name'] == 'STRING'
    assert columns[1]['nullable'] is False
    assert columns[2]['name'] == 'col3'
    assert columns[2]['type_name'] == 'DECIMAL'
    assert columns[2]['nullable'] is True
    assert columns[2]['type_precision'] == 10
    assert columns[2]['type_scale'] == 2