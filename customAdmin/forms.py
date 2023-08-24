from django import forms

from .models import *

def get_category_choice():
    categories = Category.objects.all() 
    
    CATEGORY_CHOICE = [(category.id, category.name) for category in categories]

    return CATEGORY_CHOICE

class AdminLoginForm(forms.Form):
    username = forms.CharField(label="ユーザー名")
    password = forms.CharField(label="パスワード")
    
class SiteForm(forms.Form):
    domain = forms.CharField(label="ドメイン名")
    name = forms.CharField(label="サイト名")

class PrefectureForm(forms.Form):
    name = forms.CharField(label="都道府県名")
    display_order = forms.IntegerField(label="ソート番号")

class WorkHourForm(forms.Form):
    name = forms.CharField(label="稼働率名")
    display_order = forms.IntegerField(label="ソート番号")

class WorkTypeForm(forms.Form):
    name = forms.CharField(label="勤務形態名")
    display_order = forms.IntegerField(label="ソート番号")

class CategoryForm(forms.Form):
    name = forms.CharField(label="メインカテゴリ名")
    display_order = forms.IntegerField(label="ソート番号")

    
class SubCategoryForm(forms.Form):

    category = forms.ChoiceField(choices=get_category_choice, label="メインカテゴリ")
    name = forms.CharField(label="サブカテゴリー名")
    display_order = forms.IntegerField(label="ソート番号")

    
class SkillForm(forms.Form):

    category = forms.ChoiceField(choices=get_category_choice, label="メインカテゴリ")
    name = forms.CharField(label="スキル名")

    

class EmailChangeForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")


class AccountControlForm(forms.Form):
    
    choices = [
        (2, "アクティブ"),
        (3, "入札をブロックする"),
        (4, "アカウントをブロックする"),
    ]

    status = forms.ChoiceField(choices=choices, label="状態")

