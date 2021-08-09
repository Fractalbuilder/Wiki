from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newEntry", views.createEntry, name="createEntry"),
    path("wiki/edit/<str:title>", views.editEntry, name="editEntry"),
    path("random", views.randomEntry, name="randomEntry"),
]