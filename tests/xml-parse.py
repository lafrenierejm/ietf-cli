#!/usr/bin/env python3
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    import ietf_cli.xml.parse as parse
    from ietf_cli.xml.enum import DocumentType
except:
    raise


class TestParse(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__), 'data/rfc-index.xml')
    namespace = {'index': 'http://www.rfc-editor.org/rfc-index'}

    def setUp(self):
        self.tree = ET.parse(type(self).data_file)
        self.root = self.tree.getroot()
        self.entries = parse.findall(self.root, DocumentType.RFC)

    def test_findall(self):
        self.assertEqual(3, len(self.entries))

    def test_find_doc_id(self):
        self.assertEqual(8180, parse.find_doc_id(self.entries[0]))
        self.assertEqual(10, parse.find_doc_id(self.entries[1]))
        self.assertEqual(8174, parse.find_doc_id(self.entries[2]))


if __name__ == '__main__':
    unittest.main()
