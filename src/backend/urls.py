from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/recipes", views.search_recipes_page, name="search_recipes_page"),
    path("search/country", views.search_by_country_page, name="search_by_country_page"),
    path("search/ingredient", views.search_by_ingredient_page, name="search_by_ingredient_page"),
    path('countries/<str:country>/', views.country_recipes, name='country_recipes'),
    path("recipes/<int:id>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/", views.recipe_list, name="recipes"),
    path("recipes/search/", views.search, name="search"),
]