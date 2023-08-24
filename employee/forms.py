from django import forms

from customAdmin.models import *

YEAR_EXPERIENCES = [
    (1, "1年"),
    (2, "2年"),
    (3, "3年"),
    (4, "4年"),
    (5, "5年以上"),
]


def get_skills():
    items = Skill.objects.all().order_by('category_id', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices

def get_prefectures():
    items = Prefecture.objects.all().order_by('display_order', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices


class EmployeeProfileForm(forms.Form):
    feature_image = forms.ImageField(label="ヘッダー画像", required=False)
    role = forms.CharField(label="役割")
    intro = forms.CharField(label="自己紹介", required=False)

    personal_url=forms.URLField(label="個人ウェブサイトURL", required=False)
    facebook_url=forms.URLField(label="Facebook URL", required=False)
    twitter_url=forms.URLField(label="Twitter URL", required=False)
    github_url=forms.URLField(label="Github URL", required=False)


class ExperienceForm(forms.Form):
    company = forms.CharField(label="会社名")
    role = forms.CharField(label="役割")
    comment = forms.CharField(label="コメント", required=False)
    
    start_date = forms.DateField(label="From")
    end_date = forms.DateField(label="To")

    
class SkillForm(forms.Form):
    skill = forms.ChoiceField(choices=get_skills, label="スキル")
    year = forms.ChoiceField(choices=YEAR_EXPERIENCES, label="経験年数")

    

class EmployeeSearchForm(forms.Form):    

    keyword = forms.CharField(label="Keyword")
    page = forms.IntegerField(label="page")

    address = forms.MultipleChoiceField(choices=get_prefectures, widget=forms.CheckboxSelectMultiple(), label="作業場所")