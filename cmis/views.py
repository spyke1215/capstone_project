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
        section = request.POST.get("section")
        cemetery = request.POST.get("cemetery")
            

        names = Q(first_name__iexact=first) | Q(middle_name__iexact=middle) | Q(last_name__iexact=last) | Q(lot__sections__iexact=section) | Q(lot__cemetery__name__iexact=cemetery)

        if birth == "" and death == "":
            filtered = names
        elif death == "":
            filtered = names | Q(birth_date__year=birth) 
        elif birth == "":
            filtered = names | Q(death_date__year=death)
        else:
            filtered = names | Q(birth_date__year=birth) | Q(death_date__year=death)
    
        return render(request,'cmis/search.html',{
            "deceased": Deceased.objects.filter(filtered)
        })
    
    return render(request,'cmis/search.html',{
            "deceased": Deceased.objects.all()
        })

def deceased(request):
    return render(request,'cmis/deceased.html', {
        "deceased": Deceased.objects.get(pk=2)
    })