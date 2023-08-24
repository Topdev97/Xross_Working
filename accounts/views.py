from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import os
import uuid
import pathlib

import stripe

from .models import *
from .forms import *
# Create your views here.

from utils.middlewares import employee_middleware, user_middleware


stripe.api_key = settings.STRIPE_SECRET_KEY

def register_info(request):
    
    if request.user.is_authenticated:
        user = request.user
        if(user.status == 1):
            if request.method == "POST":
                    # create a form instance and populate it with data from the request:
                    form = RegisterInfoForm(request.POST)
                    # check whether it's valid:
                    if form.is_valid():
                        # process the data in form.cleaned_data as required
                        first_name = form.cleaned_data['first_name']
                        last_name = form.cleaned_data['last_name']
                        first_name_hiragana = form.cleaned_data['first_name_hiragana']
                        last_name_hiragana = form.cleaned_data['last_name_hiragana']
                        birthday = form.cleaned_data['birthday']
                        phone = form.cleaned_data['phone']
                        prefecture = form.cleaned_data['prefecture']
                        address = form.cleaned_data['address']
                        user_type = form.cleaned_data['user_type']
                        
                        try:                            
                            user.first_name = first_name
                            user.last_name = last_name
                            user.first_name_hiragana = first_name_hiragana
                            user.last_name_hiragana = last_name_hiragana
                            user.birthday = birthday
                            user.phone = phone
                            user.prefecture_id = prefecture
                            user.address = address
                            user.user_type = user_type
                            user.status = 2
                            user.save()
                            
                            employee = Employee(user=user)
                            employee.save()

                            employer = Employer(user=user)
                            employer.save()
                            
                            return redirect("/")

                        except Exception as e:
                            print(str(e))
                    else:
                        print("error")

                # if a GET (or any other method) we'll create a blank form
            else:
                form = RegisterInfoForm()
                # model_to_dict(user)
                
            return render(request, "account/register_info.html", {"form": form})
        else:
            return redirect("/")
        
    else:
        return redirect("/")



@login_required
@user_passes_test(user_middleware, login_url="/accounts/register_info")
def accounts_basic_info(request):

    if request.method == "POST":
        form = AccountsBasicInfoForm(request.POST, request.FILES)
        user = request.user

        if form.is_valid():  
            try: 
                name = request.FILES['avatar'].name
                avatar = upload_avatar(request)
            except:
                avatar = None

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            first_name_hiragana = form.cleaned_data['first_name_hiragana']
            last_name_hiragana = form.cleaned_data['last_name_hiragana']
            birthday = form.cleaned_data['birthday']
            phone = form.cleaned_data['phone']
            prefecture = form.cleaned_data['prefecture']
            address = form.cleaned_data['address']
                    
            try:              
                if avatar:
                    user.avatar = avatar              
                user.first_name = first_name
                user.last_name = last_name
                user.first_name_hiragana = first_name_hiragana
                user.last_name_hiragana = last_name_hiragana
                user.birthday = birthday
                user.phone = phone
                user.prefecture_id = prefecture
                user.address = address
                user.user_type = user.user_type
                user.status = 2
                user.save()
                
            except Exception as e:
                print(str(e))
    else:
        user_data = model_to_dict(request.user)
        user_data['birthday'] = str(request.user.birthday)
        print(user_data)
        form = AccountsBasicInfoForm(user_data)


    return render(request, "custom_account/basic_info.html", {"form": form})



@login_required
@user_passes_test(employee_middleware, redirect_field_name="jobs_index")
def accounts_buy_points(request):
    if request.method == "POST":
        form = BuyPointForm(request.POST)
        
        # Get the token generated by Stripe.js
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')

        try:
            # # Create a charge using the token
            charge = stripe.Charge.create(
                amount=amount,  # Amount in cents
                currency='jpy',
                description='ポイント購入',
                source=token,
            )
            messages.success(request, "ポイントが正常に購入されました。")
            request.user.paypoints = request.user.paypoints + int(amount)
            request.user.save()
        except:
            messages.error(request, "支払いに問題があります。")
    else:
        form = BuyPointForm()

    return render(request, "custom_account/buy_point.html", {"form": form, "stripe_public_key": settings.STRIPE_PUBLIC_KEY })




@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_email_change(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                request.user.email = email
                request.user.save()
                messages.success(request, "メールアドレスが正常に変更されました。")
            except:
                messages.warning(request, "メールアドレスは変更できません。")
        else:
            print(form.errors)
    else:
        form = EmailChangeForm({"email": request.user.email})

    return render(request, "custom_account/email_change.html", {"form": form})


@login_required
@user_passes_test(user_middleware, redirect_field_name="jobs_index")
def accounts_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            try:
                send_mail(
                    subject,
                    message,
                    email,
                    ["proLove0212@gmail.com"],
                    fail_silently=False,
                )
                messages.success(request, "メールが正常に送信されました。")
                form = ContactForm()
            except Exception as e:
                print(str(e))
                messages.warning(request, "メールが送信できません。")
        else:
            print(form.errors)
    else:
        form = ContactForm()

    return render(request, "custom_account/contact_form.html", {"form": form})

@login_required
def accounts_menu(request):
    return render(request, "custom_account/account_menu.html")


@login_required
def upload_avatar(request):
    os.makedirs('tailwindcss/static/uploads/avatars', exist_ok=True)
    avatar_directory = 'tailwindcss/static/uploads/avatars'
    uploaded_file = request.FILES['avatar']
    filename = str(uuid.uuid4()) + pathlib.Path(uploaded_file.name).suffix

    with open(os.path.join(avatar_directory, filename), 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
        
    try:
        if request.user.avatar != "default.png":
            os.remove(os.path.join('tailwindcss/static/uploads/avatars', request.user.avatar))
    except Exception as e:
        print(str(e))
        pass

    return filename

