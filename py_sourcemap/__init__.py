from .py_sourcemap import SourcemapParser as InternalParser

name = 'py_sourcemap'

__all__ = ["SourcemapParser"]


class Token:
    def __init__(self, src_line, src_col, source, name):
        self.src_line = src_line
        self.src_col = src_col
        self.source = source
        self.name = name

    def to_tuple(self):
        return (self.source, self.src_line, self.src_col, self.name)

    def to_dict(self):
        return {
            'source': self.source,
            'src_line': self.src_line,
            'src_col': self.src_col,
            'name': self.name,
        }

    def __repr__(self):
        return '<Token: source={}, src_line={}, src_col={}, name={}>'.format(
            self.source, self.src_line, self.src_col, self.name,
        )


class SourcemapParser:
    def __init__(self, map_path):
        self.parser = InternalParser(map_path)

    def lookup(self, line, column):
        (src_line, src_col, source, name) = self.parser.original_location_for(line, column)
        return Token(src_line=src_line,
                     src_col=src_col,
                     source=source,
                     name=name)
