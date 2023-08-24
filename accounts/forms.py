from django import forms
from customAdmin.models import * 


def get_prefecture_choice():

    prefectures = Prefecture.objects.all()
    
    PREFECTURES_CHOICE = [(prefecture.id, prefecture.name) for prefecture in prefectures]

    return PREFECTURES_CHOICE

class RegisterInfoForm(forms.Form):
    
    USER_TYPE_CHOICES = [
      ("employee", '仕事を受けたい'),
      ("employer", '仕事を依頼したい'),
    ]

    first_name = forms.CharField(label="姓")
    last_name = forms.CharField(label="名")
    first_name_hiragana = forms.CharField(label="姓(せい)")
    last_name_hiragana = forms.CharField(label="名(めい)")
    birthday = forms.DateField(label="生年月日")
    address = forms.CharField(label="住所（番地まで）")
    phone = forms.CharField(label="電話番号", required=False)

    user_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=USER_TYPE_CHOICES, 
        initial="employee",
        label=""
    )
    
    prefecture = forms.ChoiceField(
        choices=get_prefecture_choice, 
        label="住所(都道府県)"
    )



class AccountsBasicInfoForm(forms.Form):
    avatar = forms.ImageField(label="プロフィール画像", required=False)
    first_name = forms.CharField(label="姓")
    last_name = forms.CharField(label="名")
    first_name_hiragana = forms.CharField(label="姓(せい)")
    last_name_hiragana = forms.CharField(label="名(めい)")
    email = forms.CharField(label="メールアドレス")
    prefecture = forms.ChoiceField(
        widget=forms.Select,
        choices=get_prefecture_choice, 
        label="住所(都道府県)"
    )
    birthday = forms.DateField(label="生年月日")
    address = forms.CharField(label="住所（番地まで）")
    phone = forms.CharField(label="電話番号", required=False)



class EmailChangeForm(forms.Form):    
    email = forms.EmailField( label="メールアドレス")


    
class ContactForm(forms.Form):    
    email = forms.EmailField( label="メールアドレス")
    subject = forms.CharField( label="件名")
    message = forms.CharField( label="メッセージ")


    
class BuyPointForm(forms.Form):
    
    BUY_TYPE_CHOICES = [
      ("5", '5pt-1000円'),
      ("10", '10pt-2000円'),
      ("20", '20pt-4000円'),
      ("50", '50pt-10000円'),
      ("100", '100pt-20000円'),
    ]
    
    points = forms.ChoiceField(
        choices=BUY_TYPE_CHOICES, 
        initial="5",
        label="購入数"
    )