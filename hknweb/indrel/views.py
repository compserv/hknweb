from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from hknweb.utils import allow_public_access

from hknweb.indrel.models import UserResume
from hknweb.models import Committeeship
import datetime

def generate_resumebook(request):
    curr_year = datetime.datetime.now().strftime("%Y")
    year_range = []
    resumes = {}
    for year in range(int(curr_year), int(curr_year) + 4):        
        by_year_users = UserResume.objects.filter(userInfo__graduation_date__year = year).values('userInfo__user__first_name', 'userInfo__user__last_name')
        by_year_names = []
        for u in by_year_users:
            by_year_names.append(f"{u['userInfo__user__last_name']}, {u['userInfo__user__first_name']}")
        
        resumes[year] = by_year_names
        if resumes[year]:
            year_range.append(year)

    
        
    
    #Edit so officers_users to grab based off on current semester, not just the first committeeship
    officers_users = Committeeship.objects.filter(committee__name = "Industrial Relations").all()[0].officers.all()
    officers_names = []
    for user in officers_users:
        officers_names.append(f"{user.first_name} {user.last_name}")
    
    letter_content = render_to_string("indrel/indrel_letter.tex", {"indrel_officers": officers_names})
    
    letter_tex = HttpResponse(letter_content, content_type="text/plain")
    letter_tex["Content-Disposition"] = 'attachment; filename="output.tex"'
    
    toc_content = render_to_string("indrel/toc.tex", {"resumes": resumes, "years": year_range})
    toc_content = HttpResponse(toc_content, content_type="text/plain")
    toc_content["Content-Disposition"] = 'attachment; filename="output.tex"'
    
    return toc_content

@allow_public_access
def indrel(request):
    return render(request, "indrel/indrel.html")
