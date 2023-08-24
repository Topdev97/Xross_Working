from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.contrib import messages
from loguru import logger
import datetime

from utils.middlewares import *
from proposal.models import *
from .models import *
from job.forms import *
from customAdmin.serializers import *
from .serializers import *


page_size = 20

def job_filter(request, type):
    keyword = keyword = request.GET.get("keyword")
    page = keyword = request.GET.get("page")
    price_min = keyword = request.GET.get("price_min")
    price_max = keyword = request.GET.get("price_max")
    category = keyword = request.GET.get("category")
    work_at = keyword = request.GET.get("work_at")
    work_hour = keyword = request.GET.get("work_hour")
    work_type = keyword = request.GET.get("work_type")
    
    m_list = Job.objects.filter(is_active=True)

    if type == "index":
        m_list = m_list.filter(applicating_until__gte=datetime.datetime.now())

    if type == "workspace":
        if request.user.user_type == "employer":
            m_list = m_list.filter(user_id=request.user.id)
        else:
            m_list = m_list.filter(id__in=[item.job_id for item in Proposal.objects.filter(user_id=request.user.id)])
            
    if type == "favourite":
        m_list = m_list.filter(id__in=[item.job_id for item in JobFavourite.objects.filter(user_id=request.user.id)])
    
    if category:
        m_list = m_list.filter(category_id__in=category)
        
    if work_at:
        m_list = m_list.filter(work_at_id__in=work_at)
        
    if work_hour:
        m_list = m_list.filter(work_hour_id__in=work_hour)
        
    if work_type:
        m_list = m_list.filter(work_type_id__in=work_type)
            
    if price_min:
        m_list = m_list.filter(price_max__gte=price_min[0])

    if price_max:
        m_list = m_list.filter(price_min__lte=price_max[0])

    if keyword:
        m_list = m_list.filter(title__contains = keyword[0], comment__contains = keyword[0])

    m_list = m_list.order_by('-created_at')

    if page:
        page = page[0]              
    else:
        page = 1

    paginator = Paginator(m_list, page_size)
    page_obj = paginator.get_page(page)  

    page_data = JobSerializer(page_obj.object_list, context={"request": request}, many=True)
    page_obj.object_list = page_data.data

    if page == page_obj.paginator.num_pages:
        st_index = (page-1)*page_size + 1
        ed_index = st_index + len(page_obj.object_list) - 1
        search_message = f"全{m_list.count()}件中{st_index}件～{ed_index}件を表示中"
    else:
        st_index = (page-1)*page_size + 1
        ed_index = (page)*page_size
        search_message = f"全{m_list.count()}件中{st_index}件～{ed_index}件を表示中"

    return {
        "page_obj": page_obj,
        "search_message" :  search_message,
        "total_count" : m_list.count()
    }

def index(request):
    form = JobSearchForm(request.GET)
    
    try:     
        rslt = job_filter(request, "index")   
        
        return render(request, "job/index.html", 
                    {
                        "form": form,
                        "page_obj": rslt['page_obj'], 
                        "search_message": rslt['search_message'] ,
                        "total_count": rslt['total_count'] 
                    })
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return render(request, "/")

@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def workspace(request):
    form = JobSearchForm(request.GET)
    
    try:     
        rslt = job_filter(request, "workspace")   
        
        return render(request, "job/index.html", 
                    {
                        "form": form,
                        "page_obj": rslt['page_obj'], 
                        "search_message": rslt['search_message'] ,
                        "total_count": rslt['total_count'] 
                    })
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return render(request, "/")


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def favourites(request):
    form = JobSearchForm(request.GET)
    
    try:     
        rslt = job_filter(request, "favourite")   
        
        return render(request, "job/index.html", 
                    {
                        "form": form,
                        "page_obj": rslt['page_obj'], 
                        "search_message": rslt['search_message'] ,
                        "total_count": rslt['total_count'] 
                    })
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return render(request, "/")



def info(request, id):
    
    try:
        m_job = Job.objects.get(id=id)
        m_skills = JobSkill.objects.filter(job_id=id)

        m_proposals = Proposal.objects.filter(job_id=id).order_by("created_at")

    except Job.DoesNotExist:
        return redirect("/jobs/search")
    
    if request.user.is_authenticated : 
        if(request.user.user_type == "employer" and m_job.user_id == request.user.id):
            return render(request, "job/info.html", {"job": m_job, "skills": m_skills, "proposals": m_proposals})
        else:
            is_bided = request.user.id in [item.user_id for item in m_proposals]
    
            return render(request, "job/info.html", {"job": m_job, "skills": m_skills, "is_bided": is_bided})
    return render(request, "job/info.html", {"job": m_job, "skills": m_skills})
        

@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def create(request):
    if request.user.user_type == "employee":
        return redirect("/accounts/basic_info")
    
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)

        if form.is_valid():

            category = form.cleaned_data['category']
            title = form.cleaned_data['title']
            comment = form.cleaned_data['comment']
            skills = form.cleaned_data['skill']
            work_at = form.cleaned_data['work_at']
            work_hour = form.cleaned_data['work_hour']
            work_type = form.cleaned_data['work_type']
            price_min = form.cleaned_data['price_min']
            price_max = form.cleaned_data['price_max']
            applicating_until = form.cleaned_data['applicating_until']
            pj_start_date = form.cleaned_data['pj_start_date']
            pj_end_date = form.cleaned_data['pj_end_date']
                
            try:    
                m_job = Job(title=title, category_id=category, comment=comment, user=request.user, price_min=price_min, price_max=price_max, applicating_until=applicating_until, pj_start_date=pj_start_date, pj_end_date=pj_end_date, work_at_id=work_at, work_hour_id=work_hour, work_type_id=work_type)
                m_job.save()
                
                for skill in skills:
                    m_job_skill = JobSkill(job=m_job, skill_id=skill)
                    m_job_skill.save()
                
                form = JobForm()
                messages.success(request, "成果的に登録されました。")
            except Exception as e:
                print(str(e))
        else:
            print(form.errors)
    else:
        form = JobForm()
    return render(request, "custom_account/new_project.html", {"form": form})

@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def like(request, id):
    job_id = id
    user_id = request.user.id
    redirect_url = request.POST.get("redirect")

    try: 
        m_job = Job.objects.get(id=id)
        if m_job.user.id == user_id:
            return redirect(redirect_url)
    except Job.DoesNotExist:
        return redirect(redirect_url)


    if request.method == "POST":
        m_like, created = JobLike.objects.get_or_create(job_id=job_id, user_id=user_id)
        if not created:
            JobLike.objects.filter(job_id=job_id, user_id=user_id).delete()
    
    return redirect(redirect_url)


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def favourite(request, id):
    job_id = id
    user_id = request.user.id
    redirect_url = request.POST.get("redirect")

    try: 
        m_job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return redirect(redirect_url)
    

    if request.method == "POST":
        favourite, created = JobFavourite.objects.get_or_create(job_id=job_id, user_id=user_id)
        if not created:
            JobFavourite.objects.filter(job_id=job_id, user_id=user_id).delete()
    

    return redirect(redirect_url)

