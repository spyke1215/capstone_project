import ast
import datetime
import json
from hashlib import blake2b

from django.db.models import Q
from django.shortcuts import render

from cmis.models import *
from django.db.models import Q
import json
import ast
import datetime
import re

# Create your views here.


def menu(request):
    return render(request, "cmis/menu.html")


def report(request):

    lot = Lot.objects.all()

    sections = Section.objects.filter(cemetery__name="Sacred Heart").count()
    total_deceased = Deceased.objects.all().count()
    total_lots = lot.count()
    unavailable_lots = lot.filter(status__name="Unavailable").count()
    available_lots = lot.filter(status__name="Vacant").count()
    reserved_lots = lot.filter(status__name="Reserved").count()
    occupied_lots = lot.filter(status__name="Occupied").count()
    columbarium = lot.filter(category__name="Columbarium").count()
    lawn = lot.filter(category__name="Lawn lot").count()
    mausoleum = lot.filter(category__name="Mausoleum").count()

    return render(
        request,
        "cmis/report.html",
        {
            "total_deceased": total_deceased,
            "total_lots": total_lots,
            "unavailable_lots": unavailable_lots,
            "vacant_lots": available_lots,
            "reserved_lots": reserved_lots,
            "occupied_lots": occupied_lots,
            "sections": sections,
            "columbarium": columbarium,
            "lawn": lawn,
            "mausoleum": mausoleum,
        },
    )


def cemetery(request):
    lot = ""
    section = ""

    lotFilter = Lot.objects.filter(section__cemetery__name=request.GET["q"])
    sectionFilter = Section.objects.filter(cemetery__name=request.GET["q"])

    if lotFilter:

        string = ""
        dict = ""

        for lot in lotFilter:

            polygon = str(lot.polygon)
            pkl = str(lot.pk)
            status = str(lot.status.name)

            string += (
                "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [["
                + polygon
                + "]]}, 'properties': {'id_lot': "
                + pkl
                + ", 'status': '"
                + status
                + "'"
            )

            graveFilter = Grave.objects.filter(Q(lot__id=pkl) & Q(lot__status=2))

            if graveFilter:
                ctr = 0
                for grave in graveFilter:
                    pkd = str(grave.deceased.pk)
                    fname = grave.deceased.first_name
                    lname = grave.deceased.last_name

                    birth = datetime.datetime.strptime(
                        str(grave.deceased.birth_date), "%Y-%m-%d"
                    ).strftime("%#b %#d, %Y")
                    death = datetime.datetime.strptime(
                        str(grave.deceased.death_date), "%Y-%m-%d"
                    ).strftime("%#b %#d, %Y")

                    string += (
                        ", 'id_deceased_"
                        + str(ctr)
                        + "': "
                        + pkd
                        + ", 'name_"
                        + str(ctr)
                        + "': '"
                        + fname
                        + " "
                        + lname
                        + "', 'birth_"
                        + str(ctr)
                        + "': '"
                        + birth
                        + "', 'death_"
                        + str(ctr)
                        + "': '"
                        + death
                        + "'"
                    )

                    ctr += 1
                string += ", 'layer': " + str(ctr) + "}},"
            else:
                string += "}},"

        dict = {"type": "FeatureCollection", "features": ast.literal_eval(string)}
        lot = json.dumps(dict)
    else:
        lot = "null"

    if sectionFilter:

        string1 = ""
        dict1 = ""

        for section in sectionFilter:

            polygon = str(section.polygon)
            pk = str(section.pk)
            section = section.name

            string1 += (
                "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [["
                + polygon
                + "]]}, 'properties': {'id': '"
                + pk
                + "','section': '"
                + section
                + "'}},"
            )

        dict1 = {"type": "FeatureCollection", "features": ast.literal_eval(string1)}
        section = json.dumps(dict1)
    else:
        section = "null"

    center = ""
    zoom = ""

    for cemetery in Cemetery.objects.filter(name=request.GET["q"]):
        center = cemetery.geolocation
        zoom = cemetery.zoom

    return render(
        request,
        "cmis/cemetery.html",
        {"lot": lot, "section": section, "center": center, "zoom": zoom},
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

        print(first)
        print(middle)
        print(last)
        print(birth)
        print(death)

        names = (
            Q(deceased__first_name__iexact=first)
            | Q(deceased__middle_name__iexact=middle)
            | Q(deceased__last_name__iexact=last)
            | Q(lot__section__name__iexact=section)
            | Q(lot__section__cemetery__name__iexact=cemetery)
        )

        if birth == "" and death == "":
            filtered = names
        elif death == "":
            filtered = names | Q(deceased__birth_date__year=birth)
        elif birth == "":
            filtered = names | Q(deceased__death_date__year=death)
        else:
            filtered = (
                names
                | Q(deceased__birth_date__year=birth)
                | Q(deceased__death_date__year=death)
            )

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

        strip = geoloc(Lot.objects.filter(pk=request.POST.get("pk")))

        return render(
            request,
            "cmis/deceased.html",
            {
                "grave": Grave.objects.filter(lot__id=request.POST.get("pk")),
                "coords": strip,
            },
        )

    else:
        strip = geoloc(Lot.objects.filter(pk=request.GET["q"]))

        return render(
            request,
            "cmis/deceased.html",
            {
                "grave": Grave.objects.filter(lot__id=request.GET["q"]),
                "coords": strip,
            },
        )


def geoloc(filter):

    grave = filter
    strip = ""
    for grave in grave:

        strip = re.sub(r"[\([{})\]]", "", str(grave.polygon)).split(",", 2)
        str(strip.pop(2))
        strip = strip[1] + "," + strip[0]
        strip = "".join(strip.split())
        print(strip)

    return strip
