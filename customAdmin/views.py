from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.admin.forms import *
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.forms import *

from utils.middlewares import *
from .models import *
from .forms import *

def admin_login(request):
    #check this request is valid
    
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials

                if user.is_superuser:
                    login(request, user)
                    return redirect("/admin/employees")
                else:
                    logout(request)
                    form.non_field_errors = "このユーザーには権限がありません。"
            else:
                # No backend authenticated the credentials
                form.non_field_errors = "スタッフアカウントの正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。"
        else:
            print(form.errors)      

    else:
        form = AdminLoginForm()

    
    return render(request, "admin/auth/login.html", {"form": form})


@user_passes_test(admin_middleware, login_url="/admin/login")
def admin_password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            form = PasswordChangeForm(request.user)
            messages.success(request, "パスワードは正常に変更されました。")
        else:
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "admin/auth/password_change.html", {"form": form})


@user_passes_test(admin_middleware, login_url="/admin/login")
def email_change(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
        else:
            print(form.errors)
    else:
        form = EmailChangeForm({"email": request.user.email})

    return render(request, "admin/auth/email_change.html", {"form": form})


@user_passes_test(admin_middleware, login_url="/admin/login")
def index(request):

    return redirect("/admin/employees")
