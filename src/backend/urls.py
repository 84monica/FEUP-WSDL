from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('countries/<str:country>/', views.country_recipes, name='country_recipes'),
    path("recipes/<int:id>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/", views.recipe_list, name="recipes"),
    path("recipes/search/", views.search, name="search"),
]