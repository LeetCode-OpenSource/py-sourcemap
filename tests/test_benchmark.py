from py_sourcemap import SourcemapParser
import sourcemap


parser = SourcemapParser('./index.js.map')
min_map = open('./index.js.map', 'r').read()
index = sourcemap.loads(min_map)


def test_py_sourcemap(benchmark):
    token = benchmark(parser.lookup, 1, 195303)
    assert token.src_line == 22
    assert token.src_col == 41
    assert token.name == 'edges'


def test_python_sourcemap(benchmark):
    token = benchmark(index.lookup, line=0, column=195302)
    assert token.src_line == 21
    assert token.src_col == 40
    assert token.name == 'edges'
