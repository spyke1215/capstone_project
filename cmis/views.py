from django.shortcuts import render
from cmis.models import *
from django.db.models import Q


# Create your views here.
def menu(request):
    return render(request,'cmis/menu.html')

def cemetery(request):
    return render(request,'cmis/cemetery.html')

def search(request):
    if request.method == "POST":

        first = request.POST.get("first")
        middle = request.POST.get("middle")
        last = request.POST.get("last")
        birth = request.POST.get("birth")
        death = request.POST.get("death")

        return render(request,'cmis/search.html',{
            "deceased": Deceased.objects.filter(Q(first_name__iexact=first) | Q(middle_name__iexact=middle) 
            | Q(last_name__iexact=last))
        })
    
    return render(request,'cmis/search.html',{
            "deceased": Deceased.objects.all()
        })
def deceased(request):
    return render(request,'cmis/deceased.html', {
        "deceased": Deceased.objects.get(pk=7)
    })