import unittest
import argparse
from unittest.mock import MagicMock
import sys
from unittest.mock import patch
import parser


class TestArgsManager(unittest.TestCase):


    def test_set_action(self):
        mock_fn = MagicMock()
        argv = ['prog', '--find']
        with patch.object(sys, 'argv', argv):
            state_parser = argparse.ArgumentParser()
            action_parser = argparse.ArgumentParser()
            arg_manager = parser.ArgManager(state_parser, action_parser, parser.ArgValues())
            (arg_manager.add_action(mock_fn, '--find', help="find home assistants within a given address range",
                action='store_true')) \
                .exec()
            self.assertTrue(mock_fn.called)

    def test_set_different_action(self):
        mock_fn = MagicMock()
        argv = ['prog', '--info']
        with patch.object(sys, 'argv', argv):
            state_parser = argparse.ArgumentParser()
            action_parser = argparse.ArgumentParser()
            arg_manager = parser.ArgManager(state_parser, action_parser, parser.ArgValues())
            (arg_manager.add_action(mock_fn, '--find', help="find home assistants within a given address range",
                action='store_true')) \
                .exec()
            self.assertFalse(mock_fn.called)


# @todo create tests for values (how to make an iterable with attrs)

if __name__=='__main__':
    unittest.main()
