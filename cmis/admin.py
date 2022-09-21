from django.contrib import admin
from .models import Deceased, Cemetery, Lot, Category

# Register your models here.
admin.site.site_header = 'Sepulcrum Administration'
admin.site.site_title = 'Sepulcrum'

admin.site.register(Deceased)
admin.site.register(Cemetery)
admin.site.register(Lot)
admin.site.register(Category)
