from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.core.paginator import Paginator

from utils.middlewares import *
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

        m_list = User.objects.filter(username__contains=keyword, user_type = 'employee', is_staff=0).order_by('username')
        
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

        return render(request, "admin/employees/index.html", {"page_obj": page_obj, "search_message": search_message ,"keyword": keyword, "page_number": page_number, "total_count": m_list.count()})
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "admin/employees/index.html")


@user_passes_test(admin_middleware, login_url="/admin/login")
def update(request):
    try:
        id = request.GET.get('id')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/employees")

    try:
        m_user = User.objects.get(id=id)
    except User.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/employees")

    if request.method == "POST":
        form = AccountControlForm(request.POST)

        if(form.is_valid()):
            status = form.cleaned_data['status']
            if status == 2:
                m_user.status = 2
                m_user.is_active = 1
                m_user.save()
            elif status == 3:
                m_user.status = 3
                m_user.is_active = 1
                m_user.save()
            elif status == 4:
                m_user.status = 4
                m_user.is_active = 0
                m_user.save()
            
            messages.success(request, "正常に完了しました。")
            
    else:
        form = AccountControlForm(model_to_dict(m_user))

    return render(request, "admin/employees/update.html", {"form": form, "current_user": m_user})


@user_passes_test(admin_middleware, login_url="/admin/login")
def delete(request):
    try:
        id = request.POST.get('id')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/employees")

    try:
        m_employer = User.objects.get(id=id)
    except User.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/employees")

    try:
        m_employer.delete()
        messages.success(request, "成果的に削除されました。")
    except:
        messages.error(request, "エラーが発生しました。")
        
    return redirect("/admin/employees")
