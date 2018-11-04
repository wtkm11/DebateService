"""
Model classes
"""
from collections import namedtuple

Opinion = namedtuple("Opinion", "name yes_percent arguments")
Argument = namedtuple("Argument", "description author")
