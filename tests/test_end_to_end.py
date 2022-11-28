# Mostly taken from ocfweb's end_to_end_test.py, since it is pretty
# comprehensive, but with some small changes to support Django's admin app:
# https://github.com/ocf/ocfweb/blob/e53c7bcdfe7096/tests/end_to_end_test.py
from typing import Iterable

from textwrap import dedent

import pytest

from django.urls import NoReverseMatch, URLPattern, reverse

from .utils import gen_safe_url_patterns


def assert_does_not_error(client, path):
    resp = client.get(path, follow=True)
    if resp.status_code not in (
        # OK!
        200,
        # Bad request. This usually happens when the view requires
        # arguments (e.g. GET params), but we don't know what to guess what to
        # provide in this test as the arguments, so 400 errors are counted as
        # passing.
        400,
    ):
        # If a SERVER_NAME is set, then we redirect off-site somewhere, we'll
        # assume these succeed.
        if "SERVER_NAME" not in resp.request:
            raise AssertionError(
                dedent(
                    """\
                    Should have received status code 200 or 400, but instead received {resp.status_code}.
                    Full path: {path}
                    Final URL: {resp.url}
                    The response body was:
                    {resp.content}
                """
                ).format(path=path, resp=resp),
            )


def _get_reversed_urlpatterns(urlpatterns: Iterable[URLPattern]):
    """Yields a list of all URLs that we can reverse with default args."""
    for urlpattern in urlpatterns:
        try:
            path = reverse(urlpattern.name, *urlpattern.default_args)
        except NoReverseMatch:
            pass
        else:
            yield path


url_patterns = [pattern for pattern, _ in gen_safe_url_patterns()]
reversed_url_patterns = _get_reversed_urlpatterns(url_patterns)

@pytest.mark.parametrize("path", reversed_url_patterns)
def test_view_does_not_error_with_default_args(client, path):
    print(path)
    assert_does_not_error(client, path)
