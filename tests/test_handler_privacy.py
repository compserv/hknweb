from typing import List, Union

from django.urls import URLPattern, URLResolver

from hknweb.urls import safe_urlpatterns

from django.test import TestCase


class HandlerPrivacyTests(TestCase):
    def _check_handler_privacy(self, handler, name):
        if getattr(handler, "_permissions", False):
            # handler is a controller func with a permission annotation
            pass
        elif hasattr(handler, "cls"):
            # handler is generated from a REST view class using .as_view()
            return self._check_handler_privacy(handler.cls, name)
        elif hasattr(handler, "view_class"):
            # handler is generated from a view class using .as_view()
            return self._check_handler_privacy(handler.view_class, name)
        elif hasattr(handler, "get_permissions"):
            # handler is from django-rest-framework
            assert handler.get_permissions(
                handler
            ), f"REST ViewSet {name} ({handler}) has insufficient permission classes: {handler.get_permissions(handler)}"
        else:
            raise Exception(f"{name} ({handler}) does not check permissions")

    def _gen_url_patterns(self, src: List[Union[URLPattern, URLResolver]], path=()):
        for elem in src:
            if isinstance(elem, URLResolver):
                yield from self._gen_url_patterns(
                    elem.url_patterns, (*path, elem.pattern)
                )
            elif isinstance(elem, URLPattern):
                yield elem.callback, (*path, elem.pattern)
            else:
                raise Exception("Unexpected resolver type", type(elem))

    def test_handler_privacy(self):
        for pattern, path in self._gen_url_patterns(safe_urlpatterns):
            self._check_handler_privacy(pattern, ",".join(map(str, path)))
