from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.core.paginator import Paginator

from utils.middlewares import *
from customAdmin.models import *
from customAdmin.forms import *
from job.models import *
from proposal.models import *
from message.models import *

page_size = 20

@user_passes_test(admin_middleware, login_url="/admin/login")
def index(request):
    try:            
        keyword = request.GET.get("keyword")
        page_number = request.GET.get("page")

        if keyword == None:  keyword=""
        if page_number == None:  page_number=1 
        else: page_number = int(page_number)

        m_list = Job.objects.filter(is_active=True)
        if keyword != "":
            m_list = m_list.filter(title__contains=keyword)
        m_list = m_list.order_by('title')
        
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

        return render(request, "admin/messages/index.html", {"page_obj": page_obj, "search_message": search_message ,"keyword": keyword, "page_number": page_number, "total_count": m_list.count()})
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "admin/messages/index.html")


@user_passes_test(admin_middleware, login_url="/admin/login")
def info(request, id):
    
    try:
        m_job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/messages")

    employee_id = request.GET.get("employee_id")

    employees = User.objects.filter(id__in=[item.user_id for item in Proposal.objects.filter(job_id = id)]).order_by("username")

    if employees.count() > 0:
        if employee_id:
            message_history = JobMessage.objects.filter(job_id=id, sender_id__in=[m_job.user.id, employee_id], receiver_id__in=[m_job.user.id, employee_id]).order_by("updated_at")
        else:
            message_history = JobMessage.objects.filter(job_id=id, sender_id__in=[m_job.user.id, employees[0].id], receiver_id__in=[m_job.user.id, employees[0].id]).order_by("updated_at")
    else:
        message_history = []

    return render(request, "admin/messages/info.html", {"employees": employees, "job": m_job, "job_messages": message_history })

