from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.db.models import F

from hknweb.utils import (
    allow_public_access,
    login_and_access_level,
    GROUP_TO_ACCESSLEVEL,
)
from hknweb.candidate.models import ShortLink
from hknweb.candidate.forms import ImportShortLinksForm, CreateShortLinkForm


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def manage_shortlinks(request):
    """
    Dedicated page for managing shortlinks.
    Accessible by candidates and officers.
    """
    shortlinks = ShortLink.objects.filter(active=True).order_by("-created_at")
    create_form = CreateShortLinkForm()
    import_form = ImportShortLinksForm()

    context = {
        "shortlinks": shortlinks,
        "create_shortlink_form": create_form,
        "import_shortlinks_form": import_form,
    }

    return render(request, "candidate/shortlinks_management.html", context)


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def create_shortlink(request):
    """
    View for creating a single shortlink.
    Accessible by candidates and officers.
    """
    if request.method == "POST":
        print(f"DEBUG: POST data received: {request.POST}")
        form = CreateShortLinkForm(request.POST)
        print(f"DEBUG: Form created, is_valid: {form.is_valid()}")

        if form.is_valid():
            print(f"DEBUG: Form is valid, data: {form.cleaned_data}")
            shortlink = form.save(commit=False)
            shortlink.created_by = request.user
            shortlink.active = True
            try:
                shortlink.save()
                print(f"DEBUG: Shortlink saved successfully: {shortlink.id}")
                messages.success(
                    request,
                    f"Shortlink created: {shortlink.slug} -> {shortlink.destination_url}",
                )
            except Exception as e:
                print(f"DEBUG: Error saving shortlink: {str(e)}")
                messages.error(request, f"Error creating shortlink: {str(e)}")
        else:
            # Display form errors
            print(f"DEBUG: Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        print(f"DEBUG: Received non-POST request: {request.method}")

    return redirect("candidate:manage_shortlinks")


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def import_shortlinks(request):
    """
    View for importing shortlinks from CSV.
    Accessible by candidates and officers.
    """
    if request.method == "POST":
        form = ImportShortLinksForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                created_count, updated_count, errors = form.save(user=request.user)

                # Display success message
                success_parts = []
                if created_count > 0:
                    success_parts.append(f"{created_count} created")
                if updated_count > 0:
                    success_parts.append(f"{updated_count} updated")

                if success_parts:
                    messages.success(
                        request, f"Shortlinks imported: {', '.join(success_parts)}"
                    )

                # Display errors if any
                if errors:
                    for error in errors[:10]:  # Limit to first 10 errors
                        messages.warning(request, error)
                    if len(errors) > 10:
                        messages.warning(
                            request, f"... and {len(errors) - 10} more errors"
                        )

            except Exception as e:
                messages.error(request, f"Error processing CSV: {str(e)}")
        else:
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    # Redirect to officer portal (both GET and POST)
    return redirect("candidate:manage_shortlinks")


@allow_public_access
def redirect_shortlink(request, slug):
    """
    Public view that redirects shortlinks to their destination.
    Also increments the click counter.
    """
    shortlink = get_object_or_404(ShortLink, slug=slug, active=True)

    # Increment click count atomically
    ShortLink.objects.filter(pk=shortlink.pk).update(click_count=F("click_count") + 1)

    # Redirect to destination
    return redirect(shortlink.destination_url)
