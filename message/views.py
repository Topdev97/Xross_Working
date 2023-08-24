from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.contrib import messages

import uuid
import os
import pathlib

from utils.middlewares import *
from job.models import *
from .models import *
from .serializers import *
from .forms import *
# Create your views here.

@login_required
@user_passes_test(employer_middleware, redirect_field_name="jobs_index")
def employer_messages(request, job_id):
    try:
        m_job = Job.objects.get(id=job_id)  
        users_list = [item.user_id for item in Proposal.objects.filter(job_id=job_id, status__in=[0, 1,2])]
        m_list = JobEmployeeMessageHistory.objects.filter(job_id=job_id, user_id__in=users_list).order_by("-updated_at")
        
        m_users = User.objects.filter(id__in=users_list)
        temp = MessageEmployeeSerializer(m_users, context={"request": request, "job_id": job_id}, many=True)
        m_user_list = list(temp.data)

        # if len(m_list) > 0:
        #     return redirect(f"/messages/employer/{job_id}/{m_list[0].user_id}")
        
        return render(request, "messages/employer_empty.html", {"job": m_job, "users": m_user_list})
    except:
        return redirect("/jobs/search")

@login_required
@user_passes_test(employer_middleware, redirect_field_name="jobs_index")
def employer_message(request, job_id, user_id):
    try:
        m_proposal = Proposal.objects.get(job_id=job_id, user_id=user_id)
        if m_proposal.status in [0, 1, 2]:
            pass
        else:
            return redirect("/jobs/search")

        m_users = User.objects.filter(id__in=[item.user_id for item in Proposal.objects.filter(job_id=job_id, status__in=[0, 1, 2])])
        temp = MessageEmployeeSerializer(m_users, context={"request": request, "job_id": job_id}, many=True)
        m_user_list = list(temp.data)

        m_user = User.objects.get(id=user_id)
        m_job = Job.objects.get(id=job_id)        
        
        if request.method == "POST":
            form = JobMessageForm(request.POST, request.FILES)
            if form.is_valid():
                
                try:
                    name = request.FILES['attachment'].name
                    attachment = upload_file(request, "attachment")
                except:
                    attachment = None

                message = form.cleaned_data['message']
                
                m_message = JobMessage(job_id=job_id, sender_id=request.user.id, receiver_id=m_user.id, message=message)
                m_message.save()

                m_job.save()

                try:
                    m_history = JobEmployeeMessageHistory.objects.get(job_id=job_id, user_id=m_user.id)
                    m_history.save()
                except JobEmployeeMessageHistory.DoesNotExist:
                    m_history = JobEmployeeMessageHistory(job_id=job_id, user_id=m_user.id)
                    m_history.save()
                
                if attachment:
                    m_attachment = AttachmentFile(message=m_message, name=name, storage_id=attachment)
                    m_attachment.save()
                
                form = JobMessageForm()
            else:
                print(form.errors)
        else:
            JobMessage.objects.filter(job_id=job_id, receiver_id=request.user.id, sender_id=m_user.id).update(receiver_readed=True)

            form = JobMessageForm()
        
        
        m_messages = JobMessage.objects.filter(job_id=job_id, sender_id__in=[m_user.id, request.user.id], receiver_id__in=[m_user.id, request.user.id]).order_by("updated_at")
        
        return render(request, "messages/employer.html", {"form": form, "job": m_job, "users": m_user_list, "current_user": m_user, "job_messages": m_messages})
    except Exception as e:
        print(str(e))
        return redirect("/jobs/search")



def take_last_message(el):
    return el['last_message']

@login_required
@user_passes_test(employee_middleware, redirect_field_name="jobs_index")
def employee_messages(request):
    m_jobs = Job.objects.filter(id__in=[item.job_id for item in Proposal.objects.filter(user_id = request.user.id, status__in=[0,1,2])])
    m_job_list = MessageEmployerSerializer(m_jobs, context={"request": request}, many=True)
    m_list = list(m_job_list.data)

    m_list.sort(key=take_last_message)
    m_list.reverse()

    # if len(m_list) > 0:
    #     return redirect(f"/messages/employee/{m_list[0]['id']}")
    
    return render(request, "messages/employee_empty.html", {"jobs": m_list})



@login_required
@user_passes_test(employee_middleware, redirect_field_name="jobs_index")
def employee_message(request, job_id):
    try:
        m_proposal = Proposal.objects.get(job_id=job_id, user_id=request.user.id)
        if m_proposal.status in [0, 1, 2]:
            pass
        else:
            return redirect("/jobs/search")

        m_jobs = Job.objects.filter(id__in=[item.job_id for item in Proposal.objects.filter(user_id = request.user.id, status__in=[0,1,2])])
        m_job_list = MessageEmployerSerializer(m_jobs, context={"request": request}, many=True)
        m_job_list = list(m_job_list.data)
        m_job_list.sort(key=take_last_message)
        m_job_list.reverse()

        m_job = Job.objects.get(id=job_id)        
        
        if request.method == "POST":
            form = JobMessageForm(request.POST, request.FILES)
            if form.is_valid():
                
                try:
                    name = request.FILES['attachment'].name
                    attachment = upload_file(request, "attachment")
                except:
                    attachment = None

                message = form.cleaned_data['message']
                
                m_message = JobMessage(job_id=job_id, sender_id=request.user.id, receiver_id=m_job.user.id, message=message)
                m_message.save()

                m_job.save()

                try:
                    m_history = JobEmployeeMessageHistory.objects.get(job_id=job_id, user_id=request.user.id)
                    m_history.save()
                except JobEmployeeMessageHistory.DoesNotExist:
                    m_history = JobEmployeeMessageHistory(job_id=job_id, user_id=request.user.id)
                    m_history.save()
                
                if attachment:
                    m_attachment = AttachmentFile(message=m_message, name=name, storage_id=attachment)
                    m_attachment.save()
                
                form = JobMessageForm()
            else:
                print(form.errors)
        else:
            JobMessage.objects.filter(job_id=job_id, receiver_id=request.user.id, sender_id=m_job.user_id).update(receiver_readed=True)

            form = JobMessageForm()
        
        
        m_messages = JobMessage.objects.filter(job_id=job_id, sender_id__in=[m_job.user_id, request.user.id], receiver_id__in=[m_job.user_id, request.user.id]).order_by("updated_at")
        
        return render(request, "messages/employee.html", {"form": form, "jobs": m_job_list, "job": m_job, "job_messages": m_messages})
    except Exception as e:
        print(str(e))
        return redirect("/messages/employee")
    


def upload_file(request, field_name):
    os.makedirs('tailwindcss/static/uploads/message_attachment', exist_ok=True)
    attach_dir = 'tailwindcss/static/uploads/message_attachment'
    uploaded_file = request.FILES[field_name]
    filename = str(uuid.uuid4()) + pathlib.Path(uploaded_file.name).suffix

    with open(os.path.join(attach_dir, filename), 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    return filename