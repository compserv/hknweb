from .utils import gen_safe_url_patterns


def check_handler_privacy(handler, name):
    if getattr(handler, "_permissions", False):
        # handler is a controller func with a permission annotation
        pass
    elif hasattr(handler, "cls"):
        # handler is generated from a REST view class using .as_view()
        return check_handler_privacy(handler.cls, name)
    elif hasattr(handler, "view_class"):
        # handler is generated from a view class using .as_view()
        return check_handler_privacy(handler.view_class, name)
    elif hasattr(handler, "get_permissions"):
        # handler is from django-rest-framework
        assert handler.get_permissions(
            handler
        ), f"REST ViewSet {name} ({handler}) has insufficient permission classes: {handler.get_permissions(handler)}"
    else:
        raise Exception(f"{name} ({handler}) does not check permissions")


def test_handler_privacy():
    for pattern, path in gen_safe_url_patterns():
        check_handler_privacy(pattern, ",".join(map(str, path)))
