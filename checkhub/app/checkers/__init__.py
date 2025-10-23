from .base import BaseChecker
from .example import ExampleChecker
from .glados import GladosChecker

CHECKER_REGISTRY = {
    "BaseChecker": BaseChecker,
    "ExampleChecker": ExampleChecker,
    "GladosChecker": GladosChecker,
}


def get_checker(checker_class: str):
    return CHECKER_REGISTRY.get(checker_class, BaseChecker)
