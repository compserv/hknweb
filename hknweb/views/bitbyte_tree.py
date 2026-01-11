from django.shortcuts import render

from hknweb.utils import allow_public_access, login_and_committee
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User

@login_and_committee(settings.COMPSERV_GROUP)
def update_bitbyte_tree(request):
    return

# TODO: dont read from the file when actual model and backend for bitbyte groups exists.
@allow_public_access
def bitbyte_tree_data(request):
    byte_bits = {}
    data = {"nodes": [], "links": []}
    all_bytes = []
    with open("hknweb/static/bit_byte_tree_data.csv", "r") as f:
        lines = f.readlines()[1::]
        for line in lines:
            line = line.strip()
            if line.split(",")[0] not in all_bytes:
                all_bytes.append(line.split(",")[0])
            if line.split(",")[1] not in all_bytes:
                all_bytes.append(line.split(",")[1])

            if not byte_bits.get(line.split(",")[0], False):
                byte_bits[line.split(",")[0]] = []
            byte_bits[line.split(",")[0]].append(line.split(",")[1])

    for byte in all_bytes:
        user = User.objects.get(username__iexact=byte)
        data["nodes"].append(
            {
                "id": byte,
                "name": user.first_name + " " + user.last_name,
                "candidate_semester": user.date_joined.year,
            }
        )

    for byte in byte_bits:
        for bit in byte_bits[byte]:
            data["links"].append({"source": byte, "target": bit})

    return JsonResponse(data)


@allow_public_access
def bitbyte_tree(request):
    return render(request, "about/bitbyte_tree.html")
