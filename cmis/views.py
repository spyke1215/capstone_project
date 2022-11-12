import ast
import json
from hashlib import blake2b

from django.db.models import Q
from django.shortcuts import render

from cmis.models import *

# Create your views here.


def menu(request):
    return render(request, "cmis/menu.html")


def cemetery(request):

    lot = ""
    section = ""

    if Lot.objects.filter(section__cemetery__name=request.GET["q"]):

        string = ""
        dict = ""

        for lot in Lot.objects.filter(
                section__cemetery__name=request.GET["q"]):

            polygon = str(lot.polygon)
            pkl = str(lot.pk)
            status = str(lot.status.name)

            string += (
                "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [["
                + polygon + "]]}, 'properties': {'id_lot': " + pkl +
                ", 'status': '" + status + "'")

            if Grave.objects.filter(pk=pkl):
                for grave in Grave.objects.filter(pk=pkl):

                    pkd = str(grave.deceased.pk)
                    fname = grave.deceased.first_name
                    lname = grave.deceased.last_name

                    string += (", 'id_deceased': " + pkd + ", 'name': '" +
                               fname + " " + lname + "'}},")

            else:
                string += "}},"

        dict = {
            "type": "FeatureCollection",
            "features": ast.literal_eval(string)
        }
        lot = json.dumps(dict)

    if Section.objects.filter(cemetery__name=request.GET["q"]):

        string1 = ""
        dict1 = ""

        for section in Section.objects.filter(cemetery__name=request.GET["q"]):

            polygon = str(section.polygon)
            pk = str(section.pk)
            name = section.name

            string1 += (
                "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [["
                + polygon + "]]}, 'properties': {'id': '" + pk +
                "','name': '" + name + "'}},")

        dict1 = {
            "type": "FeatureCollection",
            "features": ast.literal_eval(string1)
        }
        section = json.dumps(dict1)

    center = ""
    zoom = ""

    for cemetery in Cemetery.objects.filter(name=request.GET["q"]):
        center = cemetery.geolocation
        zoom = cemetery.zoom

    return render(
        request,
        "cmis/cemetery.html",
        {
            "lot": lot,
            "section": section,
            "center": center,
            "zoom": zoom
        },
    )


def search(request):
    if request.method == "POST":

        first = request.POST.get("first")
        middle = request.POST.get("middle")
        last = request.POST.get("last")
        birth = request.POST.get("birth")
        death = request.POST.get("death")
        section = request.POST.get("section")
        cemetery = request.POST.get("cemetery")

        names = (Q(deceased__first_name__iexact=first)
                 | Q(deceased__middle_name__iexact=middle)
                 | Q(deceased__last_name__iexact=last)
                 | Q(lot__section__name__iexact=section)
                 | Q(lot__section__cemetery__name__iexact=cemetery))

        if birth == "" and death == "":
            filtered = names
        elif death == "":
            filtered = names | Q(deceased__birth_date__year=birth)
        elif birth == "":
            filtered = names | Q(deceased__death_date__year=death)
        else:
            filtered = (names
                        | Q(deceased__birth_date__year=birth)
                        | Q(deceased__death_date__year=death))

        return render(
            request,
            "cmis/search.html",
            {
                "grave": Grave.objects.filter(filtered),
                "cemetery": Cemetery.objects.all(),
                "section": Section.objects.all(),
            },
        )

    else:
        return render(
            request,
            "cmis/search.html",
            {
                "grave": Grave.objects.all(),
                "cemetery": Cemetery.objects.all(),
                "section": Section.objects.all(),
            },
        )


def deceased(request):

    if request.method == "POST":

        return render(
            request,
            "cmis/deceased.html",
            {"grave": Grave.objects.get(pk=request.POST.get("pk"))},
        )

    else:

        return render(
            request,
            "cmis/deceased.html",
            {"grave": Grave.objects.get(pk=request.GET["q"])},
        )
