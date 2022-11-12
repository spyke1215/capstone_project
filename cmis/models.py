from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=32) #NAME OF CATEOGORY
    max_layers = models.IntegerField() #MAX LAYERS
    price = models.IntegerField() #PRICE

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} "

class Cemetery(models.Model):
    name = models.CharField(max_length=32) #NAME OF CEMETERY
    address = models.CharField(max_length=64) #CEMETERY ADDRESS
    geolocation = models.CharField(max_length=64)
    zoom = models.IntegerField() #ZOOM LEVEL

    class Meta:
        verbose_name_plural = "cemeteries"

    def __str__(self):
        return f"{self.name} "

class Status(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "status"
    
    def __str__(self):
        return f"{self.name}"

class Section(models.Model):
    name = models.CharField(max_length=32) #NAME OF SECTION
    polygon = models.CharField(max_length=1024)
    cemetery = models.ForeignKey(Cemetery, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "sections"

    def __str__(self):
        return f"{self.name} | {self.cemetery}"

class Lot(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #CATEGORIES
    status = models.ForeignKey(Status, on_delete=models.CASCADE) #LOT STATUS
    section = models.ForeignKey(Section, on_delete=models.CASCADE) #CEMETERY SECTION
    polygon = models.CharField(max_length=1024) #POLYGON
    
    class Meta:
        verbose_name_plural = "lots"
    
    def __str__(self):
        return f"{self.pk} | {self.category} | {self.section}"

class Deceased(models.Model):
    first_name = models.CharField(max_length=32) #FIRST NAME
    last_name = models.CharField(max_length=32) #LAST NAME
    middle_name = models.CharField(max_length=32, blank=True) #MIDDLE NAME
    birth_date = models.DateField() #BIRTH DATE
    death_date = models.DateField() #DEATH DATE
    description = models.CharField(max_length=128, null=True, blank=True) #DESCRIPTION
    image = models.ImageField(null=True, blank=True) #IMAGE

    class Meta:
            verbose_name_plural = "deceased"

    def __str__(self):
        return f"{self.pk} | {self.first_name} {self.middle_name} {self.last_name} | {self.birth_date} - {self.death_date}"

class Grave(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    deceased = models.ForeignKey(Deceased, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "graves"

    def __str__(self):
        return f"{self.pk}"