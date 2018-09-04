# py-sourcemap

[![CircleCI](https://circleci.com/gh/LeetCode-OpenSource/py-sourcemap.svg?style=svg)](https://circleci.com/gh/LeetCode-OpenSource/py-sourcemap)
[![Build Status](https://travis-ci.com/LeetCode-OpenSource/py-sourcemap.svg?branch=master)](https://travis-ci.com/LeetCode-OpenSource/py-sourcemap)
[![Build status](https://ci.appveyor.com/api/projects/status/ubn6tpgyryapy319/branch/master?svg=true)](https://ci.appveyor.com/project/Brooooooklyn/py-sourcemap/branch/master)


A tiny [source-map-mappings](https://github.com/fitzgen/source-map-mappings) bindings for python using [PyO3](https://github.com/PyO3/pyo3)

# Platform Support

### Operating Systems

| Linux  | macOS | Windows x32 | Windows x64 |
| ------ | ----- | ----------- | ----------- |
| ✓      | ✓     | ✓           | ✓           |

### Python

| Python3.5 | Python3.6 | Python3.7 |
| --------- | --------- | --------- |
| ✓         | ✓         | ✓         |

# Usage
```python
from py_sourcemap import SourcemapParser

sourcemap_parser = SourcemapParser("./tests/index.js.map")
sourcemap_parser.original_location_for(0, 195302) # (original_line, original_column, source_file_name, function_name_in_source)
```
