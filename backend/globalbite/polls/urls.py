from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipes/", views.recipe_list, name="recipes"),
    path("countries/", views.country_list, name="countries"),
    path('country/<str:country>/', views.country_recipes, name='country_recipes'),
]