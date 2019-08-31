import argparse
from argparse import SUPPRESS
import sys
import re


class ParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ArgValues:
    def setValues(self, vals):
        self._vals = vals
        return self

    def __getattr__(self, name):
        # You can manually specify the number of replacements by changing the 4th argument
        key = (re.sub("^get_(.*)$", "\\1", name))
        if key in self._vals and getattr(self._vals, key):
            return lambda : getattr(self._vals, key)[0]
        else:
            raise ParameterError('Missing argument: ' + key.replace('_', '-'))

class ArgManager:

    def __init__(self, stateParser, actionParser, argValues):
        self._argValues = argValues
        self._callbacks = {}
        self.valueParser = stateParser
        self.valueParser.usage =SUPPRESS
        self.actionParser = actionParser
        self.actionParser.usage = SUPPRESS
        self._currentAction = None


    def addValue(self, *args, **kwargs):
        self.valueParser.add_argument(*args, **kwargs)
        return self

    def addAction(self, callback, *args, **kwargs):
        self.actionParser.add_argument(*args, **kwargs)
        dest = self.actionParser._option_string_actions[args[0]].dest
        # @todo: find out how this gets replaced in argparser
        self.setAction(dest.replace('-', '_'), callback)
        return self


    def setAction(self, name, callback):
        self._callbacks[name] =  callback
        return self

    def getCurrentAction(self):
        return self._currentAction

    def exec(self):
        values, ignore = self.valueParser.parse_known_args()
        self._argValues.setValues(values)
        args, ignored = self.actionParser.parse_known_args()
        for key in vars(args):
            if getattr(args, key) and key in self._callbacks:
                self._currentAction = key.replace('_', '-')
                self._callbacks[key](self._argValues)
        return self

    def print_help(self):
        print("\nSETTINGS\n")
        self.valueParser.print_help()
        print("\nACTIONS\n")
        self.actionParser.print_help()

class ArgsManagerFactory:
    def getManager(self):
        return ArgManager(argparse.ArgumentParser(), argparse.ArgumentParser(), ArgValues())


