from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.contrib import messages

import os
import uuid
import pathlib

from utils.middlewares import *
from accounts.models import *
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
 
    form = EmployeeSearchForm(form_data)
    
    try:             
        m_list = User.objects.filter(username__contains = form_data['keyword'], user_type="employee", is_superuser = 0, status__in=[2,3,4])
            
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

        return render(request, "employee/index.html", 
                    {
                        "form": form,
                        "page_obj": page_obj, 
                        "search_message": search_message ,
                        "total_count": m_list.count(), 
                    })
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "employee/index.html")

def info(request, id):
    
    try:
        m_user = User.objects.get(id = id)
        skills = UserSkill.objects.filter(user_id = id)
        experiences = JobHistory.objects.filter(user_id = id)
    except Exception as e:
        print(str(e))
        return redirect("/jobs/search")
    
    return render(request, "employee/info.html", {"employee": m_user, "skills": skills, "experiences": experiences})



@login_required
@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_experience(request):

    m_experiences = JobHistory.objects.filter(user_id=request.user.id).order_by("-start_date")

    return render(request, "custom_account/experience.html", {"experiences": m_experiences})

@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_experience_create(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():              

            company = form.cleaned_data['company']
            role = form.cleaned_data['role']
            comment = form.cleaned_data['comment']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            history = JobHistory(user_id=request.user.id, company=company, role=role, comment=comment, start_date=start_date, end_date=end_date)
            history.save()

            form = ExperienceForm()
            messages.success(request, "正常に更新されました。")        
            
        else:
            print(form.errors)
    else:
        form = ExperienceForm()

    return render(request, "custom_account/experience_create.html", {"form": form})


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_experience_update(request):
    try:
        id = request.GET.get('id')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/accounts/experience")
    
    try:
        history = JobHistory.objects.get(user_id=request.user.id, id=id)
    except JobHistory.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/accounts/experience")

    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():              

            company = form.cleaned_data['company']
            role = form.cleaned_data['role']
            comment = form.cleaned_data['comment']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            history.company = company
            history.role = role
            history.comment = comment
            history.start_date = start_date
            history.end_date = end_date
            history.save()
            messages.success(request, "正常に更新されました。")        
            
        else:
            print(form.errors)
    else:
        temp = model_to_dict(history)
        temp['start_date'] = str(history.start_date)
        temp['end_date'] = str(history.end_date)
        form = ExperienceForm(temp)

    return render(request, "custom_account/experience_edit.html", {"form": form})



@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_experience_delete(request):
    if request.method == "POST":            
        try:
            id = request.POST.get('id')
        except:
            messages.warning(request, "リクエストのパラメータが正しくありません。")
            return redirect("/accounts/experience")
        try:        
            JobHistory.objects.filter(user_id=request.user.id, id=id).delete()
            messages.success(request, "正常に削除されました。")
        except Exception as e:
            print(str(e))
            messages.warning(request, "リクエストのパラメータが正しくありません。")
            
    return redirect("/accounts/experience")


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_skill(request):

    skills = UserSkill.objects.filter(user_id=request.user.id).order_by("-year")

    return render(request, "custom_account/skill.html", {"skills": skills})

@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_skill_create(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():              

            skill = form.cleaned_data['skill']
            year = form.cleaned_data['year']

            try:
                user_skill = UserSkill.objects.get(user_id=request.user.id, skill_id=skill)
                messages.warning(request, "すでに存在しています。")   
                return render(request, "custom_account/skill_create.html", {"form": form})
            except UserSkill.DoesNotExist:
                user_skill = UserSkill(user_id=request.user.id, skill_id=skill, year=year)
                user_skill.save()

            form = SkillForm()
            messages.success(request, "正常に更新されました。")        
            
        else:
            print(form.errors)
    else:
        form = SkillForm()

    return render(request, "custom_account/skill_create.html", {"form": form})


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_skill_update(request):
    try:
        id = request.GET.get('id')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/accounts/skill")
    
    try:
        user_skill = UserSkill.objects.get(user_id=request.user.id, id=id)
    except UserSkill.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/accounts/skill")

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():              

            skill = form.cleaned_data['skill']
            year = form.cleaned_data['year']
            
            try:
                temp = UserSkill.objects.get(user_id=request.user.id, skill_id=skill)
                user_skill.skill_id = skill
                user_skill.year = year
                user_skill.save()
                messages.success(request, "正常に更新されました。") 
            except UserSkill.DoesNotExist:  
                messages.warning(request, "存在しません。")   
                return redirect("/accounts/skill")
            
        else:
            print(form.errors)
    else:
        temp = model_to_dict(user_skill)
        form = SkillForm(temp)

    return render(request, "custom_account/skill_edit.html", {"form": form})



@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_skill_delete(request):
    if request.method == "POST":            
        try:
            id = request.POST.get('id')
        except:
            messages.warning(request, "リクエストのパラメータが正しくありません。")
            return redirect("/accounts/skill")
        try:        
            UserSkill.objects.filter(user_id=request.user.id, id=id).delete()
            messages.success(request, "正常に削除されました。")
        except Exception as e:
            print(str(e))
            messages.warning(request, "リクエストのパラメータが正しくありません。")
            
    return redirect("/accounts/skill")


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_profile(request):
    if request.user.user_type == "employer":
        return redirect("/accounts/employer_profile")

    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES)
        if form.is_valid():              
            try: 
                name = request.FILES['feature_image'].name
                feature_image = upload_feature(request)
            except Exception as e:
                print(str(e))
                feature_image = None

            role = form.cleaned_data['role']
            intro = form.cleaned_data['intro']
            github_url = form.cleaned_data['github_url']
            personal_url = form.cleaned_data['personal_url']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_url = form.cleaned_data['twitter_url']

            employee = request.user.employee
            employee.role = role
            employee.intro = intro
            employee.personal_url = personal_url
            employee.github_url = github_url
            employee.facebook_url = facebook_url
            employee.twitter_url = twitter_url

            if feature_image:
                employee.feature_image = feature_image
                
            employee.save()
            messages.success(request, "正常に更新されました。")
            
        else:
            print(form.errors)
    else:
        employer_data = model_to_dict(request.user.employee)
        form = EmployeeProfileForm(employer_data)

    return render(request, "custom_account/employee_profile.html", {"form": form})

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