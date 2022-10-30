from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=32) #NAME OF CATEOGORY
    max_layers = models.IntegerField() #MAX LAYERS
    price = models.IntegerField() #PRICE

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} "

class Cemetery(models.Model):
    name = models.CharField(max_length=32) #NAME OF CEMETERY
    longitude = models.CharField(max_length=64)
    latitude = models.CharField(max_length=64)
    address = models.CharField(max_length=64) #CEMETERY ADDRESS

    class Meta:
        verbose_name = "cemetery"
        verbose_name_plural = "cemeteries"

    def __str__(self):
        return f"{self.name} "

class Status(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "status"
    
    def __str__(self):
        return f"{self.name}"


class Lot(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #CATEGORIES
    cemetery = models.ForeignKey(Cemetery, on_delete=models.CASCADE) #CEMETERIES
    status = models.ForeignKey(Status, on_delete=models.CASCADE) #LOT STATUS
    occupied_layer = models.IntegerField() #OCCUPIED LAYERS
    geobl = models.CharField(max_length=64) #GEOLOCATION BOTTOM LEFT
    geobr = models.CharField(max_length=64) #GEOLOCATION BOTTON RIGHT
    geotr = models.CharField(max_length=64) #GEOLOCATION TOP RIGHT
    geotl = models.CharField(max_length=64) #GEOLOCATION TOP LEFT
    sections = models.CharField(max_length=10) #CEMETERY SECTION

    class Meta:
        verbose_name = "lot"
        verbose_name_plural = "lots"
    
    def __str__(self):
        return f"#{self.pk} | {self.category} | {self.cemetery} | {self.sections}"

class Deceased(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32) #FIRST NAME
    last_name = models.CharField(max_length=32) #LAST NAME
    middle_name = models.CharField(max_length=32) #MIDDLE NAME
    birth_date = models.DateField() #BIRTH DATE
    death_date = models.DateField() #DEATH DATE
    description = models.CharField(max_length=128, null=True, blank=True) #DESCRIPTION
    image = models.ImageField(null=True, blank=True) #IMAGE

    class Meta:
            verbose_name = "deceased"
            verbose_name_plural = "deceased"

    def __str__(self):
        return f"{self.pk} | {self.first_name} {self.middle_name} {self.last_name} | {self.birth_date} - {self.death_date}"