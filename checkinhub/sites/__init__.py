from .base import BaseSite, CheckinResult
from .example_site import ExampleSite
from .glados_site import GladosSite
from .hostloc_site import HostLocSite

SITE_REGISTRY = {
    'example': ExampleSite,
    'glados': GladosSite,
    'hostloc': HostLocSite,
}

__all__ = ['BaseSite', 'CheckinResult', 'SITE_REGISTRY']
