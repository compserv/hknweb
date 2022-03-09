from typing import Tuple


def check_interactivity_requirements(
    interactivities: dict,
    interactivity_requirements: dict,
) -> Tuple[bool, dict]:
    """Returns whether officer interactivities are satisfied."""
    req_remaining = {}
    for req_type, num_required in interactivity_requirements.items():
        req_remaining[req_type] = max(num_required - interactivities[req_type], 0)

    req_status = not any(req_remaining.values())

    return req_status, req_remaining
