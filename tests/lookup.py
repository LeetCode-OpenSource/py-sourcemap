from py_sourcemap import SourcemapParser

sourcemap = SourcemapParser("./tests/index.js.map")

result = sourcemap.original_location_for(0, 195302)

print(result)
