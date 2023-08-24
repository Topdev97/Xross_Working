from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.core.paginator import Paginator

from utils.middlewares import *
from job.models import *
from accounts.models import *
from customAdmin.models import *
from customAdmin.forms import *

page_size = 20


@user_passes_test(admin_middleware, login_url="/admin/login")
def index(request):
    try:            
        keyword = request.GET.get("keyword")
        page_number = request.GET.get("page")

        if keyword == None:  keyword=""
        if page_number == None:  page_number=1 
        else: page_number = int(page_number)

        m_list = Job.objects.filter(title__contains=keyword, is_active=1).order_by('-created_at')
        
        paginator = Paginator(m_list, page_size)
        page_obj = paginator.get_page(page_number)
        
        if page_number == page_obj.paginator.num_pages:
            st_index = (page_number-1)*page_size + 1
            ed_index = st_index + page_obj.object_list.count() - 1
            search_message = f"{m_list.count()}件中{st_index}件～{ed_index}件のデータが検索されました。"
        else:
            st_index = (page_number-1)*page_size + 1
            ed_index = (page_number)*page_size
            search_message = f"{m_list.count()}件中{st_index}件～{ed_index}件のデータが検索されました。"

        return render(request, "admin/jobs/index.html", {"page_obj": page_obj, "search_message": search_message ,"keyword": keyword, "page_number": page_number, "total_count": m_list.count()})
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "admin/jobs/index.html")


@user_passes_test(admin_middleware, login_url="/admin/login")
def new(request):
    try:            
        keyword = request.GET.get("keyword")
        page_number = request.GET.get("page")

        if keyword == None:  keyword=""
        if page_number == None:  page_number=1 
        else: page_number = int(page_number)

        m_list = Job.objects.filter(title__contains=keyword, is_active=0).order_by('created_at')
        
        paginator = Paginator(m_list, page_size)
        page_obj = paginator.get_page(page_number)
        
        if page_number == page_obj.paginator.num_pages:
            st_index = (page_number-1)*page_size + 1
            ed_index = st_index + page_obj.object_list.count() - 1
            search_message = f"{m_list.count()}件中{st_index}件～{ed_index}件のデータが検索されました。"
        else:
            st_index = (page_number-1)*page_size + 1
            ed_index = (page_number)*page_size
            search_message = f"{m_list.count()}件中{st_index}件～{ed_index}件のデータが検索されました。"

        return render(request, "admin/jobs/new.html", {"page_obj": page_obj, "search_message": search_message ,"keyword": keyword, "page_number": page_number, "total_count": m_list.count()})
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "admin/jobs/new.html")


@user_passes_test(admin_middleware, login_url="/admin/login")
def info(request):
    try:
        id = request.GET.get('id')
        redirect_url = request.GET.get('redirect_url')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect(redirect_url)

    try:
        m_job = Job.objects.get(id=id)
        m_skills = JobSkill.objects.filter(job_id = id)
    except Job.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect(redirect_url)
    
    return render(request, "admin/jobs/info.html", {"job": m_job, "skills": m_skills})

@user_passes_test(admin_middleware, login_url="/admin/login")
def job_active_all(request):
    
    try:
        m_job = Job.objects.filter(is_active=False)
    except Job.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/jobs")

    try:
        m_job.is_active = True
        m_job.save()
        messages.success(request, "投稿は許可されています。")
    except:
        messages.error(request, "エラーが発生しました。")
        
    return redirect("/admin/jobs")

@user_passes_test(admin_middleware, login_url="/admin/login")
def job_active(request):
    try:
        id = request.POST.get('id')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/jobs/new")

    try:
        m_job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/jobs/new")

    try:
        m_job.is_active = True
        m_job.save()
        messages.success(request, "投稿は許可されています。")
    except:
        messages.error(request, "エラーが発生しました。")
        
    return redirect("/admin/jobs/new")

@user_passes_test(admin_middleware, login_url="/admin/login")
def delete(request):
    try:
        id = request.POST.get('id')
        redirect_url = request.POST.get('redirect_url')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect(redirect_url)

    try:
        m_job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect(redirect_url)

    try:
        m_job.delete()
        messages.success(request, "成果的に削除されました。")
    except:
        messages.error(request, "エラーが発生しました。")
        
    return redirect(redirect_url)
