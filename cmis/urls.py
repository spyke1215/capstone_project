from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cemetery", views.cemetery, name="cemetery"),
    path("deceased", views.deceased, name="info"),
    path("search", views.search, name="search"),
]
