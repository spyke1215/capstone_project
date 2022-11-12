from django.contrib import admin

from .models import *

# Register your models here.
admin.site.site_header = "Sepulcrum Administration"
admin.site.site_title = "Sepulcrum"


@admin.register(Deceased)
class DeceasedAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "middle_name",
        "last_name",
        "birth_date",
        "death_date",
    )


@admin.register(Cemetery)
class CemeteryAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "geolocation")
    search_fields = ("name", "address", "geolocation")


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "section", "status")
    list_filter = ("category", "section", "status")
    search_fields = ("id", "category", "section", "status")
    ordering = ("id",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "max_layers", "price")
    search_fields = ("name", "max_layers", "price")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "cemetery")
    search_fields = ("name", "cemetery")


@admin.register(Grave)
class GraveAdmin(admin.ModelAdmin):
    list_display = ("lot", "deceased")
    search_fields = ("lot", "deceased")
