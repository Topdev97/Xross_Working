from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.contrib import messages

from utils.middlewares import *
from job.models import *
from message.models import *
from .forms import *
from .models import *
# Create your views here.

@user_passes_test(proposal_middleware, login_url="/accounts/login")
def new(request, id):
    
    try:
        m_job = Job.objects.get(id=id)
        m_skills = JobSkill.objects.filter(job_id=id)
    except Job.DoesNotExist:
        return redirect("/jobs/search")
    
    if(m_job.user.id ==  request.user.id):
        return redirect(f"/jobs/{id}")
    
    if Proposal.objects.filter(job_id=id, user_id=request.user.id).count() > 0:
        return redirect(f"/jobs/{id}")

    if request.method == "POST":
        if(request.user.points+request.user.paypoints==0):
            messages.warning(request, "ポイントが足りません。ポイントを購入してください。")
        else:    
            form = ProposalForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                price = form.cleaned_data['price']

                try:
                    m_proposal = Proposal(comment=comment, price=price, user=request.user, job_id=id)
                    m_proposal.save()

                    m_message = JobMessage(sender=m_job.user, receiver=request.user, job=m_job, message=m_job.comment)
                    m_message.save()

                    m_message = JobMessage(sender=request.user, receiver=m_job.user, job=m_job, message=comment)
                    m_message.save()

                    if request.user.points > 0:
                        request.user.points = request.user.points - 1
                        request.user.save()
                    else:
                        request.user.paypoints = request.user.paypoints - 1
                        request.user.save()
                    
                    m_job.save()

                    try:
                        m_history = JobEmployeeMessageHistory.objects.get(job_id=m_job.id, user_id=request.user.id)
                        m_history.save()
                    except JobEmployeeMessageHistory.DoesNotExist:
                        m_history = JobEmployeeMessageHistory(job_id=m_job.id, user_id=request.user.id)
                        m_history.save()

                    messages.success(request, "メッセージを成果的に伝えました。")
                    return redirect("/jobs/search")
                except Exception as e:
                    print(str(e))
                    messages.error(request, "エラーが発生しました。")

            else:
                print(form.errors)
            
    else:
        form = ProposalForm()
    return render(request, "proposal/new.html", {"form": form, "job": m_job, "skills": m_skills})


@login_required
@user_passes_test(employer_middleware, redirect_field_name="jobs_index")
def proposal_status(request):
    
    if request.method == "POST":
        job_id = request.POST["j_id"]
        user_id = request.POST["u_id"]
        status = request.POST['status']
        
        try:
            m_job = Job.objects.get(id=int(job_id))
            if m_job.user_id == request.user.id:
                pass
            else:
                messages.warning(request, "このアクションに対する許可がありません")
                return redirect(f"/jobs/{job_id}")
            
            m_pro = Proposal.objects.get(job_id=int(job_id), user_id=user_id)
            m_pro.status = int(status)
            m_pro.save()
        except Exception as e:
            print(str(e))
            pass

        return redirect(f"/jobs/{job_id}")