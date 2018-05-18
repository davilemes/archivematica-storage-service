"""Django REST Libary (DRL)"""

from .resources import Resources, ReadonlyResources
from .routebuilder import RouteBuilder
from . import utils

drl = RouteBuilder()

__all__ = ('drl', 'utils', 'Resources', 'ReadonlyResources')
