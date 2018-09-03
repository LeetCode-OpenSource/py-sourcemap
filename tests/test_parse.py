from unittest import TestCase

from py_sourcemap import SourcemapParser


class TestParser(TestCase):
    def setUp(self):
        self.sourcemap = SourcemapParser("./tests/index.js.map")

    def test_parse_trace(self):
        result = self.sourcemap.original_location_for(0, 195302)
        self.assertEqual(result[0], 22)
        self.assertEqual(result[1], 41)
        self.assertEqual(result[2][-13:], 'TopicList.jsx')
        self.assertEqual(result[3], 'edges')
