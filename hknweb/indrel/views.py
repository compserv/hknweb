from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from hknweb.utils import login_and_permission

from hknweb.utils import allow_public_access
from django.conf import settings
from hknweb.indrel.models import UserResume, ResumeBook
from hknweb.models import Committeeship
import datetime
import subprocess
import os

from PyPDF2 import PdfWriter


@login_and_permission("indrel.view_userresume")
def generate_resumebook(request):
    # Data for TOC and Years
    curr_year = datetime.datetime.now().strftime("%Y")
    year_range = []
    resumes = {}
    for year in range(int(curr_year), int(curr_year) + 4):
        by_year_users = UserResume.objects.filter(
            userInfo__graduation_date__year=year
        ).values("userInfo__user__first_name", "userInfo__user__last_name", "pdf")
        by_year_names = {}
        for u in by_year_users:
            by_year_names.update(
                {
                    f"{u['userInfo__user__last_name']}, {u['userInfo__user__first_name']}": os.path.join(
                        settings.MEDIA_ROOT, u["pdf"]
                    )
                }
            )

        resumes[year] = by_year_names
        if resumes[year]:
            year_range.append(year)
    data = [(year, resumes[year].keys()) for year in year_range]

    # Data for Indrel Message
    # Edit so officers_users to grab based off on current semester, not just the first committeeship
    officers_users = (
        Committeeship.objects.filter(committee__name="Industrial Relations")
        .all()[0]
        .officers.all()
    )
    officers_names = []
    for user in officers_users:
        officers_names.append(f"{user.first_name} {user.last_name}")

    # Generate LaTeX content
    letter_content = render_to_string(
        "indrel/indrel_letter.tex", {"indrel_officers": officers_names}
    )
    toc_content = render_to_string("indrel/toc.tex", {"data": data})
    title_contents = []
    for year in year_range:
        title_contents.append(
            (year, render_to_string("indrel/section_title.tex", {"year": year}))
        )

    # Folder for resumebooks and temporary files that will be deleted at the end
    resumebook_dir = os.path.join(settings.MEDIA_ROOT, "indrel", "resumebook")
    os.makedirs(resumebook_dir, exist_ok=True)

    # pdflatex process
    try:
        # Creates the pdfs in the directory with a specific name
        subprocess.run(
            [
                "pdflatex",
                "-output-directory",
                resumebook_dir,
                "-jobname",
                "indrel_letter",
            ],
            input=letter_content.encode(),
            check=True,
        )
        subprocess.run(
            ["pdflatex", "-output-directory", resumebook_dir, "-jobname", "toc"],
            input=toc_content.encode(),
            check=True,
        )
        for title_content in title_contents:
            subprocess.run(
                [
                    "pdflatex",
                    "-output-directory",
                    resumebook_dir,
                    "-jobname",
                    f"{title_content[0]}_Title",
                ],
                input=title_content[1].encode(),
                check=True,
            )

        # Define the paths to the generated PDFs
        letter_pdf_path = os.path.join(resumebook_dir, "indrel_letter.pdf")
        toc_pdf_path = os.path.join(resumebook_dir, "toc.pdf")
        title_pdf_paths = {}
        for year, _ in title_contents:
            title_pdf_paths.update(
                {year: os.path.join(resumebook_dir, f"{year}_Title.pdf")}
            )

        # Using PyPDF2 to merge the resumebook together
        merger = PdfWriter()

        cover_pdf_path = os.path.join(
            settings.MEDIA_ROOT, "indrel", "resumebook", "cover.pdf"
        )

        total_pdfs = [cover_pdf_path, letter_pdf_path, toc_pdf_path]
        for year in year_range:
            total_pdfs.append(title_pdf_paths[year])
            for res in resumes[year].values():
                total_pdfs.append(res)
        for pdf in total_pdfs:
            merger.append(pdf)

        resumebook_path = os.path.join(resumebook_dir, "resumebook.pdf")
        merger.write(resumebook_path)
        merger.close()

        # Return the merged PDF as a response
        with open(resumebook_path, "rb") as resumebook_pdf:
            resumebook_pdf_content = resumebook_pdf.read()

        resumebook = HttpResponse(
            resumebook_pdf_content, content_type="application/pdf"
        )
        resumebook["Content-Disposition"] = 'attachment; filename="output.pdf"'

        return resumebook
    except subprocess.CalledProcessError as error:
        print(f"Error during pdflatex: {error}")
        return HttpResponse("Error during Latex->PDF", status=500)
    finally:
        # Removing temp files in media/indrel/resumebook
        os.remove(letter_pdf_path)
        os.remove(toc_pdf_path)
        temp_suffix = [".log", ".aux", ".out"]
        for suffix in temp_suffix:
            os.remove(letter_pdf_path.replace(".pdf", suffix))
            os.remove(toc_pdf_path.replace(".pdf", suffix))
        for path in title_pdf_paths.values():
            os.remove(path)
            for suffix in temp_suffix:
                os.remove(path.replace(".pdf", suffix))


@allow_public_access
def indrel(request):
    return render(request, "indrel/indrel.html")


@login_and_permission("indrel.view_userresume")
def indrelportal(request):
    return render(request, "indrel/portal.html")


@login_and_permission("indrel.view_userresume")
def resumebooks(request):
    
    context = {
        "books": None
        
        
    }
    
    return render(request, "indrel/resumebooks.html", context=context)
