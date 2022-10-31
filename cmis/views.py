from hashlib import blake2b
from django.shortcuts import render
from cmis.models import *
from django.db.models import Q
import json
import ast

# Create your views here.
def menu(request):
    return render(request,'cmis/menu.html')

def cemetery(request):

    y = ''
    x = ''
    pkl = ''
    polygon = ''

    for lot in Lot.objects.all():

        polygon = str(lot.polygon)
        pkl = str(lot.pk)

        y += "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [["+polygon+"]]}, 'properties': {'id_lot': "+pkl+""

        if Grave.objects.filter(pk=pkl) :
            for grave in Grave.objects.filter(pk=pkl):
            
                pkd = str(grave.deceased.pk)
                fname = grave.deceased.first_name
                lname = grave.deceased.last_name

                y += ", 'id_deceased': "+pkd+", 'name': '"+fname+" "+lname+"'}},"

        else:
            y += "}},"
    
    x = {'type': 'FeatureCollection', 'features': ast.literal_eval(y)}
    lot = json.dumps(x)

    y = ''
    x = ''

    for section in Section.objects.all():

        polygon = str(section.polygon)
        pk = str(section.pk)
        name = section.name

        y += "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [["+polygon+"]]}, 'properties': {'id': '"+pk+"','name': '"+name+"'}},"
    
    x = {'type': 'FeatureCollection', 'features': ast.literal_eval(y)}
    section = json.dumps(x)

    return render(request,'cmis/cemetery.html', {
        "lot": lot,
        "section": section
    })

def search_deceased(request):
    if request.method == "POST":

        first = request.POST.get("first")
        middle = request.POST.get("middle")
        last = request.POST.get("last")
        birth = request.POST.get("birth")
        death = request.POST.get("death")
        section = request.POST.get("section")
        cemetery = request.POST.get("cemetery")
            
        names = Q(deceased__first_name__iexact=first) | Q(deceased__middle_name__iexact=middle) | Q(deceased__last_name__iexact=last) | Q(lot__sections__name__iexact=section) | Q(lot__cemetery__name__iexact=cemetery)

        if birth == "" and death == "":
            filtered = names
        elif death == "":
            filtered = names | Q(deceased__birth_date__year=birth) 
        elif birth == "":
            filtered = names | Q(deceased__death_date__year=death)
        else:
            filtered = names | Q(deceased__birth_date__year=birth) | Q(deceased__death_date__year=death)
    
        return render(request,'cmis/search_deceased.html',{
            "grave": Grave.objects.filter(filtered),
            "cemetery": Cemetery.objects.all(),
            "section": Section.objects.all()
        })
    
    return render(request,'cmis/search_deceased.html',{
            "grave": Grave.objects.all(),
            "cemetery": Cemetery.objects.all(),
            "section": Section.objects.all()
        })

def search_lot(request): #not working
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

def deceased(request): #need to show multiple deceased. use grave table

    return render(request,'cmis/deceased.html', {
        "deceased": Deceased.objects.get(pk=request.GET['q'])
    })