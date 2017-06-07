import os

import tatsu
from tatsu.ast import AST

from taskwizard.grammar import grammar_ebnf


def parse(*args, **kwargs):
    grammar = tatsu.compile(grammar_ebnf)
    return grammar.parse(*args, **kwargs, asmodel=False, semantics=Semantics(), parseinfo=True)


class TaskParser:

    def __init__(self, definition_dir):
        self.definition_dir = definition_dir
        self.task_file_path = os.path.join(definition_dir, "task.txt")

    def parse(self):
        return parse(open(self.task_file_path).read(), rule="unit")


class Semantics:

    def _default(self, ast, *args, **kwargs):
        if isinstance(ast, AST):
            return AbstractSyntaxNode(ast, *args, **kwargs)
        else:
            return ast


class AbstractSyntaxNode:

    def __init__(self, ast, *args, **kwargs):
        self.parseinfo = None
        for key, value in ast.items():
            setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._arguments = args

    def accept(self, visitor):
        method_name = "visit_%s" % self.parseinfo.rule
        if hasattr(visitor, method_name):
            method = getattr(visitor, method_name)
        else:
            method = visitor.visit_default
        return method(self)
