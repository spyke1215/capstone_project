from django.shortcuts import render
from cmis.models import *

# Create your views here.
def index(request):
    return render(request,'cmis/index.html')

def cemetery(request):
    return render(request,'cmis/cemetery.html')

def search(request):

    return render(request,'cmis/search.html',{
        "deceased": Deceased.objects.all()
    })

def deceased(request):
    return render(request,'cmis/deceased.html', {
        "deceased": Deceased.objects.get(pk=1)
    })