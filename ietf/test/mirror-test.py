#!/usr/bin/env python3
import os
import sys
import unittest
from ietf.cmd.mirror import assemble_rsync


class TestAssembleRsync(unittest.TestCase):
    boilerplate = ['rsync', '-az', '--delete-during']

    rsync_no_path = (('charter', boilerplate +
                      ['ietf.org::everything-ftp/ietf/']),
                     ('conflict', boilerplate +
                      ['rsync.ietf.org::everything-ftp/conflict-reviews/']),
                     ('draft', boilerplate +
                      ["--exclude='*.xml'",
                       "--exclude='*.pdf'",
                       'rsync.ietf.org::internet-drafts']),
                     ('iana', boilerplate +
                      ['rsync.ietf.org::everything-ftp/iana/']),
                     ('iesg', boilerplate + ['rsync.ietf.org::iesg-minutes/']),
                     ('rfc', boilerplate +
                      ["--exclude='tar*'",
                       "--exclude='search*'",
                       "--exclude='PDF-RFC*'",
                       "--exclude='tst/'",
                       "--exclude='pdfrfc/'",
                       "--exclude='internet-drafts/'",
                       "--exclude='ien/'",
                       'ftp.rfc-editor.org::everything-ftp/in-notes/']),
                     ('status', boilerplate +
                      ['rsync.ietf.org::everything-ftp/status-changes/']))

    def test_assemble_rsync(self):
        test_path = '/sample/path'
        for doc_type, cmd_array in self.rsync_no_path:

            expected_path = test_path + '/' + doc_type
            expected_cmd = cmd_array + [expected_path]

            returned_cmd, returned_path = assemble_rsync(doc_type, test_path,
                                                         False)

            self.assertEqual(expected_cmd, returned_cmd)
            self.assertEqual(expected_path, returned_path)

    def test_assemble_rsync_flat(self):
        expected_path = '/sample/path'
        for doc_type, cmd_array in self.rsync_no_path:

            expected_cmd = cmd_array + [expected_path]

            returned_cmd, returned_path = assemble_rsync(doc_type,
                                                         expected_path, True)

            self.assertEqual(expected_cmd, returned_cmd)
            self.assertEqual(expected_path, returned_path)


if __name__ == '__main__':
    unittest.main()
