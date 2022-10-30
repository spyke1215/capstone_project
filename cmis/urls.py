from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("cemetery", views.cemetery, name="cemetery"),
    path("deceased", views.deceased, name="deceased"),
    path("search_deceased", views.search_deceased, name="search_deceased"),
    path("search_lot", views.search_lot, name="search_lot"),
]
