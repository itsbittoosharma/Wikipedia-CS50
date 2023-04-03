from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("newpage",views.newpage,name="newpage"),
    path("wiki/<str:title>/edit",views.editpage,name="editpage"),
    path("random",views.random,name="random")
]
