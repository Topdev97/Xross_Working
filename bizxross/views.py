from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "base/landing.html")


def guide(request):
    return render(request, "base/guide.html")
