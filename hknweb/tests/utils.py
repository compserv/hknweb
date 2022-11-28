from typing import List, Union

from django.urls import URLPattern, URLResolver

from hknweb.urls import safe_urlpatterns


def gen_url_patterns(src: List[Union[URLPattern, URLResolver]], path=()):
    for elem in src:
        if isinstance(elem, URLResolver):
            yield from gen_url_patterns(elem.url_patterns, (*path, elem.pattern))
        elif isinstance(elem, URLPattern):
            yield elem.callback, (*path, elem.pattern)
        else:
            raise Exception("Unexpected resolver type", type(elem))


def gen_safe_url_patterns():
    yield from gen_url_patterns(safe_urlpatterns)
