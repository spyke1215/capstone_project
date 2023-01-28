from django.contrib import admin

from .models import *
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

# Register your models here.
admin.site.site_header = "Sepulcrum Administration"
admin.site.site_title = "Sepulcrum"

class DeceasedAdmin(admin.ModelAdmin):
    @admin.action(description='Generate PDF table')
    def generatePDF(modeladmin, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        # container for the 'Flowable' objects
        elements = []
        elements.append(Spacer (1, 20))
        elements.append(Paragraph("Sepulcrum Administration", ParagraphStyle(name='Normal', fontName='Helvetica-Bold', fontSize=24, alignment=TA_CENTER)))
        elements.append(Spacer (1, 20))
        elements.append(Paragraph("Deceased Reports", ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=18, alignment=TA_CENTER)))
        elements.append(Spacer (1, 30))
        elements.append(Paragraph("Total: "+ str(len(queryset)), ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=12, alignment=TA_RIGHT)))
        elements.append(Spacer (1, 5))
        
        data = [["ID", "FIRST NAME", "MIDDLE NAME", "LAST NAME", "BIRTH DATE", "DEATH DATE"]]

        for deceased in queryset:
            data.append([deceased.id, deceased.first_name, deceased.middle_name, deceased.last_name, str(deceased.birth_date), str(deceased.death_date)])
        
        t=Table(data)
        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                    ('ALIGN', (1,1), (-1,-1), 'CENTER')
                                    ]))
        elements.append(t)
        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='deceasedreports.pdf')

    list_display = (
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "birth_date",
        "death_date",
    )

    search_fields = ("first_name", "middle_name", "last_name", "birth_date", "death_date")
    ordering = ("id",)
       
    actions = [generatePDF]
admin.site.register(Deceased, DeceasedAdmin)

    
class CemeteryAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "address", "geolocation")
    search_fields = ("id", "name", "address", "geolocation")

admin.site.register(Cemetery, CemeteryAdmin)


class LotAdmin(admin.ModelAdmin):
    @admin.action(description='Generate PDF table')
    def generatePDF(modeladmin, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        # container for the 'Flowable' objects
        elements = []
        elements.append(Spacer (1, 20))
        elements.append(Paragraph("Sepulcrum Administration", ParagraphStyle(name='Normal', fontName='Helvetica-Bold', fontSize=24, alignment=TA_CENTER)))
        elements.append(Spacer (1, 20))
        elements.append(Paragraph("Lot Reports", ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=18, alignment=TA_CENTER)))
        elements.append(Spacer (1, 30))
        elements.append(Paragraph("Total: "+ str(len(queryset)), ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=12, alignment=TA_RIGHT)))
        elements.append(Spacer (1, 5))

        data = [["ID", "CATEGORY" , "SECTION", "CEMETERY", "STATUS"]]

        for lot in queryset:
            data.append([lot.id, lot.category, lot.section.name, lot.section.cemetery.name, lot.status])
        
        t=Table(data,hAlign='CENTER')
        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                    ('ALIGN', (1,1), (-1,-1), 'CENTER')
                                    ]))
        elements.append(t)
        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='lotreports.pdf')

    list_display = ("id", "category", "section", "status")
    list_filter = ("category", "section", "status")
    search_fields = ("id", "category", "section", "status")
    ordering = ("id",)

    
    actions = [generatePDF]
admin.site.register(Lot, LotAdmin)

class CategoryAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "max_layers", "price")
    search_fields = ("id", "name", "max_layers", "price")

admin.site.register(Category, CategoryAdmin)

class StatusAdmin(admin.ModelAdmin):
   
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name", )

admin.site.register(Status, StatusAdmin)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cemetery")
    search_fields = ("id", "name", "cemetery")


class GraveAdmin(admin.ModelAdmin):
    @admin.action(description='Generate PDF table')
    def generatePDF(modeladmin, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # container for the 'Flowable' objects
        elements = []

        elements.append(Spacer (1, 20))
        elements.append(Paragraph("Sepulcrum Administration", ParagraphStyle(name='Normal', fontName='Helvetica-Bold', fontSize=24, alignment=TA_CENTER)))
        elements.append(Spacer (1, 20))
        elements.append(Paragraph("Grave Reports", ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=18, alignment=TA_CENTER)))
        elements.append(Spacer (1, 30))
        elements.append(Paragraph("Total: "+ str(len(queryset)), ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=12, alignment=TA_RIGHT)))
        elements.append(Spacer (1, 5))

        data = [["ID", "FIRST NAME", "MIDDLE NAME", "LAST NAME", "BIRTHDATE", "DEATHDATE", "SECTION", "CEMETERY"]]

        for grave in queryset:
            data.append([grave.id, grave.deceased.first_name, grave.deceased.middle_name,  grave.deceased.last_name, grave.deceased.birth_date, grave.deceased.death_date, grave.lot.section.name, grave.lot.section.cemetery.name])
        
        t=Table(data,hAlign='CENTER')
        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                    ('ALIGN', (1,1), (-1,-1), 'CENTER')
                                    ]))
        elements.append(t)
        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='gravereports.pdf')

    list_display = ("id", "lot", "deceased")
    search_fields = ("id", "lot", "deceased")
    ordering = ("id",)
    actions = [generatePDF]
admin.site.register(Grave, GraveAdmin)