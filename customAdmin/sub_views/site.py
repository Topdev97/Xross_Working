from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.sites.models import Site

from utils.middlewares import *
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

        m_list = Site.objects.filter(name__contains=keyword).order_by('name')
        
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

        return render(request, "admin/sites/index.html", {"page_obj": page_obj, "search_message": search_message ,"keyword": keyword, "page_number": page_number, "total_count": m_list.count()})
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "admin/sites/index.html")


@user_passes_test(admin_middleware, login_url="/admin/login")
def update(request):
    try:
        id = request.GET.get('id')
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/sites")

    try:
        m_site = Site.objects.get(id=id)
    except Site.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/sites")

    if request.method == "POST":
        form = SiteForm(request.POST)

        if(form.is_valid()):
            domain = form.cleaned_data['domain']
            name = form.cleaned_data['name']
            
            try:
                m_site = Site.objects.get(name=name, domain=domain)
                
                if(m_site.id != id):
                    raise Site.DoesNotExist
                
                messages.error(request, "すでに存在します。")
            except Site.DoesNotExist:
                try:
                    m_site.domain = domain
                    m_site.name = name
                    m_site.save()
                    messages.success(request, "成果的に更新されました。")
                except:
                    messages.error(request, "エラーが発生しました。")
            
    else:
        form = SiteForm(model_to_dict(m_site))

    return render(request, "admin/sites/update.html", {"form": form})

