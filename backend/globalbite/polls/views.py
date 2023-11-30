from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from .models import Recipe

# Create your views here.´

def index(request):
    template = loader.get_template("polls/homePage.html")

    # Query to get the count of recipes for each country
    countries_with_counts = Recipe.objects.values('country_of_origin').annotate(recipe_count=Count('id'))

    # Sort countries in descending order based on recipe count
    sorted_countries = sorted(countries_with_counts, key=lambda x: x['recipe_count'], reverse=True)

    context = {
        "countries": [country['country_of_origin'] for country in sorted_countries],
    }

    return HttpResponse(template.render(context, request))

def country_recipes(request, country):
    template = loader.get_template("polls/recipes.html")
    context = {
        "recipes": Recipe.objects.filter(country_of_origin=country),
    }
    return HttpResponse(template.render(context, request))

def recipe_list(request):
    template = loader.get_template("polls/recipes.html")
    context = {
        "recipes": Recipe.objects.all(),
    }
    return HttpResponse(template.render(context, request))
