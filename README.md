[![Github Actions Status](https://github.com/godatadriven/pyarrow-unity/workflows/test/badge.svg)](https://github.com/godatadriven/pyarrow-unity/actions/workflows/test.yml)


## pyarrow-unity

This library provides functions to convert Pyarrow schema to Unity Catalog schema.  

## Installation
```bash
pip install pyarrow-unity
```

## Functions
**model_unity_schema(schema)**
Converts a Pyarrow schema to a list of Unity Catalog columns.  

**Parameters:**  
- schema: The Pyarrow schema to convert.
 
**Returns:**
A list of Column objects representing the Unity Catalog schema.

**Example:**
```python
import pyarrow as pa
from pyarrow_unity.model import model_unity_schema

schema = pa.schema([
    pa.field('col1', pa.int32(), nullable=True),
    pa.field('col2', pa.string(), nullable=False),
    pa.field('col3', pa.decimal128(10, 2), nullable=True)
])

columns = model_unity_schema(schema)
for column in columns:
    print(f"Name: {column.name}, Type: {column.type_name}, Nullable: {column.nullable}")
```

## License
This project is licensed under the MIT License - see the [LICENSE](license) file for details.