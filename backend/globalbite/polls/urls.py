from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('country/<str:country>/', views.country_recipes, name='country_recipes'),
    path("recipes/", views.recipe_list, name="recipes"),
]