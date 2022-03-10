from typing import Callable


def apply_to_dicts(fn: Callable, *ds: list) -> dict:
    for k, v in ds[0].items():
        if isinstance(v, dict):
            apply_to_dicts(fn, *[d[k] for d in ds])
        else:
            fn(k, v, *ds)
    return ds[0]
