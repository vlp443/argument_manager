from  argparse import ArgumentParser
from argparse import SUPPRESS
import re
import  parser
# from injector import Injector, inject



class ParameterError(Exception):
    pass

class ActionError(Exception):
    pass

class ArgValues:

    def __init__(self):
        self._vals = None

    def set_values(self, vals):
        self._vals = vals
        return self

    def __getattr__(self, name, mandatory = True):
        # You can manually specify the number of replacements by changing the 4th argument
        key = (re.sub("^get_(.*)$", "\\1", name))
        if key in self._vals and getattr(self._vals, key):
            return lambda: getattr(self._vals, key)[0]
        if(mandatory):
            raise ParameterError('Missing argument: ' + key.replace('_', '-'))
        return False;


class ArgManager:
  #  @inject
    def __init__(self, state_parser: ArgumentParser, actionParser : ArgumentParser, argValues: ArgValues):
        self._arg_values = argValues
        self._callbacks = {}
        self.value_parser = state_parser
        self.value_parser.usage = SUPPRESS
        self.action_parser = actionParser
        self.action_parser.usage = SUPPRESS
        self._current_action = None
        self._default_action = None

    def add_value(self, *args, **kwargs):
        self.value_parser.add_argument(*args, **kwargs)
        return self

    def set_default_action(self, action):
        self._default_action = action
        return self

    def add_action(self, callback, *args, **kwargs):
        self.action_parser.add_argument(*args, **kwargs)
        # @todo: either subclass action parser to gain true access to this or find another way
        dest = self.action_parser._option_string_actions[args[0]].dest
        # @todo: find out how this gets replaced in argparser
        self.set_action(dest.replace('-', '_'), callback)
        return self


    def set_action(self, name, callback):
        self._callbacks[name] = callback
        return self

    def get_current_action(self):
        return self._current_action

    def exec(self):
        values, ignore = self.value_parser.parse_known_args()
        self._arg_values.set_values(values)
        args, ignored = self.action_parser.parse_known_args()
        method_called = False
        for key in vars(args):
            if getattr(args, key) and key in self._callbacks:
                method_called = True
                self._current_action = key.replace('_', '-')
                self._callbacks[key](self._arg_values)
        if not method_called:
            if self._default_action:
                self._default_action(self._arg_values)
            else:
                raise ActionError('Nothing to do')
        return self

    def print_help(self):
        print("\nSETTINGS\n")
        self.value_parser.print_help()
        print("\nACTIONS\n")
        self.action_parser.print_help()


def get_manager():
    return ArgManager(ArgumentParser(add_help=False), ArgumentParser(add_help=False), ArgValues())

    # injector = Injector()
    # return injector.get(ArgManager)
