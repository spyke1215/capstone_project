from hashlib import blake2b
from django.shortcuts import render
from cmis.models import *
from django.db.models import Q
import json
import ast


# Create your views here.
def menu(request):
    return render(request,'cmis/menu.html')

def graves(request):

    bl = ""
    br = ""
    tr = ""
    tl = ""
    y = ''

    for item in Lot.objects.all():

        bl = item.geobl
        br = item.geobr
        tr = item.geotr
        tl = item.geotl

        y += "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[["+bl+"],["+br+"],["+tr+"],["+tl+"],["+bl+"]]]}, 'properties': {'id': '4'}},"

    # a Python object (dict):
    x = {'type': 'FeatureCollection', 'features': ast.literal_eval(y)}

    # convert into JSON:
    jsdata = json.dumps(x)
    print(jsdata)

    return render(request,'cmis/graves.html', {
        "data": jsdata
    })

def cemetery(request):
    return render(request,'cmis/cemetery.html')

def search_deceased(request):
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
    
        return render(request,'cmis/search_deceased.html',{
            "deceased": Deceased.objects.filter(filtered),
            "cemetery": Cemetery.objects.all(),
        })
    
    return render(request,'cmis/search_deceased.html',{
            "deceased": Deceased.objects.all(),
            "cemetery": Cemetery.objects.all()
        })

def search_lot(request):
    if request.method == "POST":

        category = request.POST.get("category")
        cemetery = request.POST.get("cemetery")
        status = request.POST.get("status")
        layer = request.POST.get("layer")
        section = request.POST.get("section")
    
        return render(request,'cmis/search_lot.html',{
            "lot": Lot.objects.filter(Q(category__name__iexact=category) | Q(cemetery__name__iexact=cemetery) | Q(status__name__iexact=status) | Q(occupied_layer__iexact=layer) | Q(sections__iexact=section)),
            "category": Category.objects.all(),
            "status": Status.objects.all(),
            "cemetery": Cemetery.objects.all()
        })

    return render(request,'cmis/search_lot.html',{
        "lot": Lot.objects.all(),
        "category": Category.objects.all(),
        "status": Status.objects.all(),
        "cemetery": Cemetery.objects.all()
    })

def deceased(request):
    return render(request,'cmis/deceased.html', {
        "deceased": Deceased.objects.get(pk=request.POST.get("pk"))
    })