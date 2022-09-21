from django.shortcuts import render

from cmis.models import Deceased, Category, Lot, Cemetery

# Create your views here.
def index(request):
    return render(request,'cmis/index.html')

def cemetery(request):
    return render(request,'cmis/cemetery.html')

def search(request):
    return render(request,'cmis/search.html')

def deceased(request):
    return render(request,'cmis/deceased.html', {
        "deceased": Deceased.objects.get(pk=1)
    })
