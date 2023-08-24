from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.core.paginator import Paginator

from utils.middlewares import *
from customAdmin.models import *
from customAdmin.forms import *
from customAdmin.serializers import *

page_size = 20

def get_all_categories():
    m_list = Category.objects.all().order_by('display_order', 'name')        
    
    return m_list
    

@user_passes_test(admin_middleware, login_url="/admin/login")
def index(request):
    try:            
        keyword = request.GET.get("keyword")
        page_number = request.GET.get("page")

        if keyword == None:  keyword=""
        if page_number == None:  page_number=1 
        else: page_number = int(page_number)

        m_list = Category.objects.filter(name__contains=keyword).order_by('display_order', 'name')
        
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

        return render(request, "admin/categories/index.html", {"page_obj": page_obj, "search_message": search_message ,"keyword": keyword, "page_number": page_number, "total_count": m_list.count()})
    except Exception as e:
        print(str(e))
        messages.warning(request, "リクエストのパラメータが正しくありません。")

    return render(request, "admin/categories/index.html")


@user_passes_test(admin_middleware, login_url="/admin/login")
def create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if(form.is_valid()):
            name = form.cleaned_data['name']
            display_order = form.cleaned_data['display_order']
            try:
                m_category = Category.objects.get(name=name)
                messages.error(request, "すでに存在します。")
            except Category.DoesNotExist:
                try:                        
                    m_category = Category(name = name, display_order=display_order)
                    m_category.save()

                    messages.success(request, "成果的に登録されました。")
                    form = CategoryForm()
                except:
                    messages.error(request, "エラーが発生しました。")
    else:
        form = CategoryForm()

    return render(request, "admin/categories/create.html", {"form": form})


@user_passes_test(admin_middleware, login_url="/admin/login")
def update(request):
    try:
        id = request.GET.get('id')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/categories")

    try:
        m_category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/categories")

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if(form.is_valid()):
            name = form.cleaned_data['name']
            display_order = form.cleaned_data['display_order']
            
            try:
                m_category = Category.objects.get(name=name)
                
                if(m_category.id != id):
                    raise Category.DoesNotExist
                
                messages.error(request, "すでに存在します。")
            except Category.DoesNotExist:
                try:
                    m_category.name = name
                    m_category.display_order=display_order
                    m_category.save()
                    messages.success(request, "成果的に更新されました。")
                except:
                    messages.error(request, "エラーが発生しました。")
            
    else:
        form = CategoryForm(model_to_dict(m_category))

    return render(request, "admin/categories/update.html", {"form": form})


@user_passes_test(admin_middleware, login_url="/admin/login")
def delete(request):
    try:
        id = request.POST.get('id')
    except:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/categories")

    try:
        m_category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        messages.warning(request, "リクエストのパラメータが正しくありません。")
        return redirect("/admin/categories")

    try:
        m_category.delete()
        messages.success(request, "成果的に削除されました。")
    except:
        messages.error(request, "エラーが発生しました。")
        
    return redirect("/admin/categories")
