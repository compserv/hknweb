from django.shortcuts import render

from hknweb.utils import allow_public_access
import os

@allow_public_access
def indrel(request):
    # company_names = ['Google', 'Microsoft', 'Berkeley', 'Amazon'] 
    # company_urls = ['https://google.com', 'https://microsoft.com', 'https://berkeley.edu', 'https://amazon.com']
    # company_files = ['', '', '', ''] 

    data_path = "/hknweb/static/img/sponsors/"
    metadata_file = data_path + "metadata"

    image_filepath = "/img/sponsors/"

    current_companies = [] 
    with open(os.getcwd() + metadata_file, "r") as f:
        for index, line in enumerate(f.readlines()): 
            current_name, current_url, current_filename = line.split()
            current_companies.append((index, current_name, current_url, image_filepath + current_filename))


    a = 0 
    context = {
        "company_data": current_companies
    }

    return render(request, "indrel.html", context)
