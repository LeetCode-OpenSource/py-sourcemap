from unittest import TestCase

from py_sourcemap import SourcemapParser


class TestParser(TestCase):
    def setUp(self):
        self.parser = SourcemapParser('./tests/index.js.map')

    def test_parse_trace(self):
        token = self.parser.lookup(1, 195303)
        self.assertEqual(token.src_line, 22)
        self.assertEqual(token.src_col, 41)
        self.assertEqual(token.source[-13:], 'TopicList.jsx')
        self.assertEqual(token.name, 'edges')
