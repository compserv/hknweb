from django.shortcuts import render

from hknweb.candidate.models import BitByteGroup
from hknweb.utils import allow_public_access, login_and_committee
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User


@login_and_committee(settings.COMPSERV_GROUP)
def update_bitbyte_tree(request):
    return

@allow_public_access
def bitbyte_tree_data(request):
    groups = BitByteGroup.objects.prefetch_related("bits", "bytes").all()

    username_to_node = {}
    links = []

    for group in groups:
        group_bytes = group.bytes.all()
        group_bits = group.bits.all()

        def add_to_nodes(user_list):
            for user in user_list:
                if user.username not in username_to_node:
                    username_to_node[user.username] = {
                        "id": user.username,
                        "name": f"{user.first_name} {user.last_name}",
                        "candidate_semester": user.date_joined.year,
                    }

        add_to_nodes(group_bytes)
        add_to_nodes(group_bits)

        for byte in group_bytes:
            for bit in group_bits:
                links.append({
                    "source": byte.username,
                    "target": bit.username
                })

    data = {
        "nodes": list(username_to_node.values()),
        "links": links
    }

    return JsonResponse(data)


@allow_public_access
def bitbyte_tree(request):
    return render(request, "about/bitbyte_tree.html")
