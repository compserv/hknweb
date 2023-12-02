from django.shortcuts import render

from hknweb.utils import allow_public_access
import os 

@allow_public_access
def indrel_admin(request):
    post_data = {} 
    data_path = "/hknweb/static/img/sponsors/"
    metadata_file = data_path
    if request.method == 'POST': 
        print(request.POST)
        for key in request.POST.keys():
            post_data[key] = request.POST.get(key, "") 
        metadata_file += "metadata"
        write_metadata(post_data, os.getcwd() + metadata_file, data_path, request) 


    
    
    metadata_file = data_path + "metadata"

    

    current_companies = [] 
    
    print(os.getcwd())
    
    with open(os.getcwd() + metadata_file, "r") as f:
        for index, line in enumerate(f.readlines()): 
            current_name, current_url, current_filename = line.split()
            current_companies.append((index, current_name, current_url, current_filename))

    
   

    context = {
        "company_data": current_companies
    }


    return render(request, "indrel_admin.html", context)



def write_metadata(data, filepath, file_save_path, request): 
    count = 0 
    for key in data: 
        if key.startswith("name"): 
            count += 1
    with open(filepath, 'w') as f:
        for i in range(count): 
            name = data[f"name_{i}"]
            url = data[f"url_{i}"]
            if name == "" or url == "": 
                continue 
            uploaded_image = request.FILES.get(f"file_{i}", None)
            filename = name + ".png"
            if uploaded_image: 
                with open(os.getcwd() + file_save_path + filename, 'wb') as destination:
                    for chunk in uploaded_image.chunks(): 
                        destination.write(chunk)


            
            f.write(name + " " + url + " " + filename + "\n")
        
    return "Successfully wrote to metadata file!"


