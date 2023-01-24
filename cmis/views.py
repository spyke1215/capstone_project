import ast
import datetime
import json
import re
from hashlib import blake2b
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render

from cmis.models import *

# Create your views here.


def menu(request):
    return render(request, "cmis/menu.html")


def report(request):

    if request.method == "GET":

        return render(request, "cmis/report.html",{
            "cemetery": Cemetery.objects.all()
        })


    if request.method == "POST":
        selected = request.POST.get("cemetery")
        lot = Lot.objects.filter(section__cemetery__name=selected)
        sections = Section.objects.filter(cemetery__name=selected).count()
        total_deceased = Grave.objects.filter(lot__section__cemetery__name=selected).count()
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
                "cemetery": Cemetery.objects.all(),
                "selectedCemetery": selected
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
            category = lot.category.name
            price = str(lot.category.price)
            layers = str(lot.category.max_layers)
            section = lot.section.name

            string += (
                "{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [["
                + polygon + "]]}, 'properties': {'id_lot': " + pkl +
                " , 'section': '" + section + "' , 'status': '" + status +
                "' , 'category': '" + category + "', 'price': '" + price +
                "', 'layers': '" + layers + "'")

            graveFilter = Grave.objects.filter(lot__id=pkl)

            if graveFilter:
                ctr = 0
                for grave in graveFilter:
                    pkd = str(grave.deceased.pk)
                    fname = grave.deceased.first_name
                    lname = grave.deceased.last_name

                    birth = datetime.datetime.strptime(
                        str(grave.deceased.birth_date),
                        "%Y-%m-%d").strftime("%#b %#d, %Y")
                    death = datetime.datetime.strptime(
                        str(grave.deceased.death_date),
                        "%Y-%m-%d").strftime("%#b %#d, %Y")

                    string += (", 'id_deceased_" + str(ctr) + "': " + pkd +
                               ", 'name_" + str(ctr) + "': '" + fname + " " +
                               lname + "', 'birth_" + str(ctr) + "': '" +
                               birth + "', 'death_" + str(ctr) + "': '" +
                               death + "'")

                    ctr += 1
                string += "}},"
            else:
                string += "}},"

        dict = {
            "type": "FeatureCollection",
            "features": ast.literal_eval(string)
        }
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
                + polygon + "]]}, 'properties': {'id': '" + pk +
                "','sections': '" + section + "'}},")

        dict1 = {
            "type": "FeatureCollection",
            "features": ast.literal_eval(string1)
        }
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

        if section == "":
            names = (Q(lot__section__cemetery__name__iexact=cemetery)
                    | Q(lot__section__name__iexact=section)
                    | Q(deceased__first_name__iexact=first)
                    | Q(deceased__middle_name__iexact=middle)
                    | Q(deceased__last_name__iexact=last)
                    )
        else: 
            names = (Q(lot__section__name__iexact=section)
                    | Q(deceased__first_name__iexact=first)
                    | Q(deceased__middle_name__iexact=middle)
                    | Q(deceased__last_name__iexact=last)
                    )

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

        graveList = Grave.objects.filter(filtered)
        page = request.GET.get('page', 1)

        paginator = Paginator(graveList, 100)
        try:
            grave = paginator.page(page)
        except PageNotAnInteger:
            grave = paginator.page(1)
        except EmptyPage:
            grave = paginator.page(paginator.num_pages)

        return render(
            request,
            "cmis/search.html",
            {
                "grave": grave,
                "cemetery": Cemetery.objects.all(),
                "section": Section.objects.filter(cemetery__name=cemetery),
                "selectedFirst": first,
                "selectedMiddle": middle,
                "selectedLast": last,
                "selectedBirth": birth,
                "selectedDeath": death,
                "selectedSection": section,
                "selectedCemetery": cemetery,
            },
        )

    else:
        graveList = Grave.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(graveList, 100)
        try:
            grave = paginator.page(page)
        except PageNotAnInteger:
            grave = paginator.page(1)
        except EmptyPage:
            grave = paginator.page(paginator.num_pages)

        return render(
            request,
            "cmis/search.html",
            {
                "grave": grave,
                "cemetery": Cemetery.objects.all(),
                "section": Section.objects.all(),
            },
        )


def searchlot(request):
    if request.method == "POST":
        
        category = request.POST.get("category")
        section = request.POST.get("section")
        status = request.POST.get("status")
        layers = request.POST.get("layers")
        cemetery = request.POST.get("cemetery")

        if section == "":
            filtered = (Q(category__name__iexact=category)
                        | Q(section__name__iexact=section)
                        | Q(status__name__iexact=status)
                        | Q(category__max_layers__iexact=layers)
                        | Q(section__cemetery__name__iexact=cemetery))
        else:
            filtered = (Q(category__name__iexact=category)
                        | Q(section__name__iexact=section)
                        | Q(status__name__iexact=status)
                        | Q(category__max_layers__iexact=layers))

        lotList = Lot.objects.filter(filtered)
        page = request.POST.get('page', 1)

        paginator = Paginator(lotList, 25)
        try:
            lot = paginator.page(page)
        except PageNotAnInteger:
            lot = paginator.page(1)
        except EmptyPage:
            lot = paginator.page(paginator.num_pages)

        return render(
            request,
            "cmis/searchlot.html",
            {
                "lot": lot,
                "cemetery": Cemetery.objects.all(),
                "section":  Section.objects.all(),
                "category": Category.objects.all(),
                "status": Status.objects.all(),
                "selectedCategory": category,
                "selectedSection": section,
                "selectedStatus": status,
                "selectedLayers": layers,
                "selectedCemetery": cemetery,
            },
        )

    else:
        lotList = Lot.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(lotList, 100)
        try:
            lot = paginator.page(page)
        except PageNotAnInteger:
            lot = paginator.page(1)
        except EmptyPage:
            lot = paginator.page(paginator.num_pages)

        return render(
            request,
            "cmis/searchlot.html",
            {
                "lot": lot,
                "cemetery": Cemetery.objects.all(),
                "section": Section.objects.all(),
                "category": Category.objects.all(),
                "status": Status.objects.all(),
            },
        )


def information(request):

    if request.method == "POST":

        strip = geoloc(Lot.objects.filter(pk=request.POST.get("pk")))

        return render(
            request,
            "cmis/information.html",
            {
                "grave": Grave.objects.filter(lot__id=request.POST.get("pk")),
                "lot": Lot.objects.filter(pk=request.POST.get("pk")),
                "coords": strip,
            },
        )

    else:
        strip = geoloc(Lot.objects.filter(pk=request.GET["q"]))

        return render(
            request,
            "cmis/information.html",
            {
                "grave": Grave.objects.filter(lot__id=request.GET["q"]),
                "lot": Lot.objects.filter(pk=request.GET["q"]),
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
