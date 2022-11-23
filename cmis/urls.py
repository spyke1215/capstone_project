from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("cemetery", views.cemetery, name="cemetery"),
    path("deceased", views.deceased, name="deceased"),
    path("search", views.search, name="search"),
    path("report", views.report, name="report"),
]
