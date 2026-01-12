from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django.db import transaction
from django.contrib.auth.models import User

import io
import csv
from hknweb.coursesemester.models import Semester
from hknweb.candidate.models import BitByteGroup
from hknweb.forms import CsvImportForm

@admin.register(BitByteGroup)
class BitByteGroupAdmin(admin.ModelAdmin):
    change_list_template = "admin/candidate/bitbyte_group_change_list.html"

    fields = ["semester", "bytes", "bits"]
    list_display = (
        "semester",
        "bytes_usernames",
        "bits_usernames",
    )
    list_filter = ["semester"]
    search_fields = [
        "bytes__username",
        "bytes__first_name",
        "bytes__last_name",
        "bits__username",
        "bits__first_name",
        "bits__last_name",
    ]
    autocomplete_fields = ["bytes", "bits"]

    def bytes_usernames(self, obj):
        return ", ".join([user.username for user in obj.bytes.all()])

    def bits_usernames(self, obj):
        return ", ".join([user.username for user in obj.bits.all()])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name="import_csv"),
        ]
        return custom_urls + urls

    # Refactor and move this outside of admin panel if this becomes front facing feature(i.e. you
    # want evp creating bitbyte groups)
    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)  # Skip header

                try:
                    # If an error happens we just don't do anything
                    with transaction.atomic():
                        count = 0
                        for row in csv.reader(io_string, delimiter=";"):
                            if not row or len(row) != 4:
                                continue

                            byte_usernames, bit_usernames, year, sem = [s.strip() for s in row]

                            semester_obj = Semester.objects.get(year=year, semester=sem)
                            group = BitByteGroup.objects.create(semester=semester_obj)
                            for byte in byte_usernames.split(","):
                                byte_user = User.objects.filter(username__iexact=byte).first()
                                group.bytes.add(byte_user)

                            for bit in bit_usernames.split(","):
                                bit_user = User.objects.filter(username__iexact=bit).first()
                                group.bits.add(bit_user)

                            count += 1
                        self.message_user(request, f"Successfully imported {count} relationships.")
                        return redirect("..")
                except Exception as e:
                    self.message_user(request, f"Error: {e}", level=messages.ERROR)

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/candidate/bitbyte_group_csv_upload.html", payload)