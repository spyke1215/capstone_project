from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("cemetery", views.cemetery, name="cemetery"),
    path("information", views.information, name="information"),
    path("search", views.search, name="search"),
    path("searchlot", views.searchlot, name="searchlot")
]
