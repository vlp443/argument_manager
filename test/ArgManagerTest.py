import unittest
import argparse
from unittest.mock import MagicMock
import sys
from unittest.mock import patch
import parser


class TestArgsManager(unittest.TestCase):



    def test_set_action(self):
        mockFn = MagicMock()
        argv = ['prog', '--find']
        with patch.object(sys, 'argv', argv):
            stateParser = argparse.ArgumentParser()
            actionParser = argparse.ArgumentParser()
            argManager = parser.ArgManager(stateParser, actionParser, parser.ArgValues())
            argManager.addAction(mockFn, '--find', help="find home assistants within a given address range", action='store_true').exec()
            self.assertTrue(mockFn.called)

    def test_set_different_action(self):
        mockFn = MagicMock()
        argv = ['prog', '--info']
        with patch.object(sys, 'argv', argv):
            stateParser = argparse.ArgumentParser()
            actionParser = argparse.ArgumentParser()
            argManager = parser.ArgManager(stateParser, actionParser, parser.ArgValues())
            argManager.addAction(mockFn, '--find', help="find home assistants within a given address range", action='store_true').exec()
            self.assertFalse(mockFn.called)

# @todo create tests for values (how to make an iterable with attrs)

if __name__ == '__main__':
    unittest.main()


