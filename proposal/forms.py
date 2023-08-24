from django import forms
from django.forms.models import model_to_dict
import json
from customAdmin.models import * 
from customAdmin.serializers import *


class ProposalForm(forms.Form):    
    comment = forms.CharField( label="コメント", required=True)
    price = forms.IntegerField(label="希望月額単価(万円)", required=True)
