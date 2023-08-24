from django import forms
from django.forms.models import model_to_dict
import json
from customAdmin.models import * 
from customAdmin.serializers import *


class JobMessageForm(forms.Form):    
    message = forms.CharField( label="コメント", required=False)
    attachment = forms.FileField( label="File", required=False)
