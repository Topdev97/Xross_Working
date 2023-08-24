from django import forms


from customAdmin.models import *

def get_prefectures():
    items = Prefecture.objects.all().order_by('display_order', 'name')   
    choices = [(item.id, item.name) for item in items]
    return choices

class EmployerProfileForm(forms.Form):
    feature_image = forms.ImageField(label="ヘッダー画像", required=False)
    company_name = forms.CharField(label="会社名")
    seo_name = forms.CharField(label="代表者名")
    intro = forms.CharField(label="会社業務")
    publish_at = forms.DateField(label="設立日")
    address = forms.CharField(label="会社住所")
    google_map_url=forms.URLField(label="GoogleMapの埋め込みURL")

    company_url=forms.URLField(label="会社WebサイトURL", required=False)
    facebook_url=forms.URLField(label="Facebook URL", required=False)
    twitter_url=forms.URLField(label="Twitter URL", required=False)
    github_url=forms.URLField(label="Github URL", required=False)


class EmployerSearchForm(forms.Form):    

    keyword = forms.CharField(label="Keyword")
    page = forms.IntegerField(label="page")

    address = forms.MultipleChoiceField(choices=get_prefectures, widget=forms.CheckboxSelectMultiple(), label="作業場所")