from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

import os
import uuid
import pathlib

from utils.middlewares import *
from accounts.models import *
from employee.models import *
from .models import *
from .forms import *

# Create your views here.
page_size = 20
  
def index(request):
    form_data = dict(request.GET)
    if("keyword" not in form_data.keys()):form_data['keyword'] = [""]
    if("page" not in form_data.keys()): form_data['page'] = [1]
    if("address" not in form_data.keys()):form_data['address'] = []

    form_data['keyword']=form_data['keyword'][0]
    form_data['page']=int(form_data['page'][0])
 
    form = EmployerSearchForm(form_data)
    
    try:             
        m_list = User.objects.filter(username__contains = form_data['keyword'], user_type="employer", is_superuser = 0, status__in=[2,3,4])
            
        if len(form_data['address']) != 0:
            m_list = m_list.filter(prefecture_id__in=form_data['address'])
            
        m_list = m_list.order_by('created_at')
            
        
        paginator = Paginator(m_list, page_size)
        page_obj = paginator.get_page(form_data['page'])        
        
        
        if form_data['page'] == page_obj.paginator.num_pages:
            st_index = (form_data['page']-1)*page_size + 1
            ed_index = st_index + page_obj.object_list.count() - 1
            search_message = f"全{m_list.count()}人中{st_index}人～{ed_index}人を表示中"
        else:
            st_index = (form_data['page']-1)*page_size + 1
            ed_index = (form_data['page'])*page_size
            search_message = f"全{m_list.count()}人中{st_index}人～{ed_index}人を表示中"

        return render(request, "employer/index.html", 
                    {
                        "form": form,
                        "page_obj": page_obj, 
                        "search_message": search_message ,
                        "total_count": m_list.count(), 
                    })
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "employer/index.html")

def info(request, id):
    
    try:
        m_user = User.objects.get(id = id)
    except Exception as e:
        print(str(e))
        return redirect("/jobs/search")
    
    return render(request, "employer/info.html", {"employer": m_user})


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_profile(request):
    if request.user.user_type == "employee":
        return redirect("/accounts/employee_profile")


    if request.method == "POST":
        form = EmployerProfileForm(request.POST, request.FILES)
        if form.is_valid():              
            try: 
                name = request.FILES['feature_image'].name
                feature_image = upload_feature(request)
            except Exception as e:
                print(str(e))
                feature_image = None

            company_name = form.cleaned_data['company_name']
            seo_name = form.cleaned_data['seo_name']
            intro = form.cleaned_data['intro']
            publish_at = form.cleaned_data['publish_at']
            google_map_url = form.cleaned_data['google_map_url']
            address = form.cleaned_data['address']
            github_url = form.cleaned_data['github_url']
            company_url = form.cleaned_data['company_url']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_url = form.cleaned_data['twitter_url']

            employer = request.user.employer
            employer.company_name = company_name
            employer.seo_name = seo_name
            employer.intro = intro
            employer.publish_at = publish_at
            employer.address = address
            employer.google_map_url = google_map_url
            
            employer.company_url = company_url
            employer.github_url = github_url
            employer.facebook_url = facebook_url
            employer.twitter_url = twitter_url

            if feature_image:
                employer.feature_image = feature_image
                
            employer.save()
            messages.success(request, "正常に更新されました。")
        else:
            print(form.errors)
    else:
        employer_data = model_to_dict(request.user.employer)
        employer_data['publish_at'] = str(request.user.employer.publish_at)
        form = EmployerProfileForm(employer_data)

    return render(request, "custom_account/employer_profile.html", {"form": form})

def upload_feature(request):
    os.makedirs('tailwindcss/static/uploads/features', exist_ok=True)
    avatar_directory = 'tailwindcss/static/uploads/features'
    uploaded_file = request.FILES['feature_image']
    filename = str(uuid.uuid4()) + pathlib.Path(uploaded_file.name).suffix

    with open(os.path.join(avatar_directory, filename), 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    try:
        if request.user.employer.feature_image != "default.png":
            os.remove(os.path.join('tailwindcss/static/uploads/features', request.user.employer.feature_image))
    except Exception as e:
        print(str(e))
        pass
    
    return filename