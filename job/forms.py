from django import forms
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from customAdmin.models import * 
from customAdmin.serializers import *


def get_skills():
    items = Skill.objects.all().order_by('category_id', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices

def get_categories():
    items = Category.objects.all().order_by('display_order', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices

def get_prefectures():
    items = Prefecture.objects.all().order_by('display_order', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices

def get_workhours():
    items = WorkHour.objects.all().order_by('display_order', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices

def get_worktypes():
    items = WorkType.objects.all().order_by('display_order', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices

class JobForm(forms.Form):    
    category = forms.ChoiceField(choices=get_categories, label="カテゴリー")
    title = forms.CharField(label="タイトル")
    comment = forms.CharField( label="コメント")
    skill = forms.MultipleChoiceField(choices=get_skills, label="スキル")
    price_min = forms.IntegerField(label="最低価格(万円)")
    price_max = forms.IntegerField(label="最高価格(万円)")

    work_at = forms.ChoiceField(choices=get_prefectures, label="作業場所")
    work_hour = forms.ChoiceField(choices=get_workhours, label="稼働率")
    work_type = forms.ChoiceField(choices=get_worktypes, label="勤務形態")
    
    applicating_until = forms.DateField(label="応募期限")
    pj_start_date = forms.DateField(label="プロジェクト開始日")
    pj_end_date = forms.DateField(label="プロジェクト終了日")
    

    def clean_price_max(self):
        try:
            price_min = self.cleaned_data['price_min']
        except:
            price_min = 0
        
        price_max = self.cleaned_data['price_max']
        if price_min and price_max and price_max <= price_min:
            raise ValidationError('金額を確認してください。')
        return price_max

    def clean_pj_start_date(self):
        try:
            applicating_until = self.cleaned_data['applicating_until']
        except:
            applicating_until = 0

        pj_start_date = self.cleaned_data['pj_start_date']
        if applicating_until and pj_start_date and pj_start_date <= applicating_until:
            raise ValidationError('プロジェクト開始日を確認してください。')
        return pj_start_date
    
    def clean_pj_end_date(self):
        try:
            pj_start_date = self.cleaned_data['pj_start_date']
        except:
            pj_start_date = 0
            
        pj_start_date = self.cleaned_data['pj_start_date']
        pj_end_date = self.cleaned_data['pj_end_date']
        if pj_start_date and pj_end_date and pj_end_date <= pj_start_date:
            raise ValidationError('プロジェクトの終了日を確認してください。')
        return pj_end_date
    
    
class JobSearchForm(forms.Form):    
    category = forms.MultipleChoiceField(choices=get_categories, widget=forms.CheckboxSelectMultiple(), label="カテゴリー")

    keyword = forms.CharField(label="Keyword")
    page = forms.IntegerField(label="page")

    price_min = forms.IntegerField(label="最低価格(万円)", min_value=0, max_value=500)
    price_max = forms.IntegerField(label="最高価格(万円)", min_value=0, max_value=500)

    work_at = forms.MultipleChoiceField(choices=get_prefectures, widget=forms.CheckboxSelectMultiple(), label="作業場所")
    work_hour = forms.MultipleChoiceField(choices=get_workhours, widget=forms.CheckboxSelectMultiple(), label="稼働率")
    work_type = forms.MultipleChoiceField(choices=get_worktypes, widget=forms.CheckboxSelectMultiple(), label="勤務形態")

    def clean_price_max(self):
        price_min = self.cleaned_data['price_min']
        price_max = self.cleaned_data['price_max']
        if price_min and price_max and price_max <= price_min:
            raise ValidationError('Maximum price must be greater than minimum price.')
        return price_max