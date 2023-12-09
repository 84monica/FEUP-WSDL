from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Q
from .models import Recipe
import ast

# Create your views here.´

def index(request):
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    template = loader.get_template("polls/homePage.html")

    if order_by == 'alphabetical':
        # Query to get the count of recipes for each country
        countries = Recipe.objects.values('country_of_origin')

        # Sort countries in alphabetical order
        sorted_countries = sorted(countries, key=lambda x: x['country_of_origin'])
        
    elif order_by == 'popularity':
        # Query to get the count of recipes for each country
        countries_with_counts = Recipe.objects.values('country_of_origin').annotate(recipe_count=Count('id'))

        # Sort countries in descending order based on recipe count
        sorted_countries = sorted(countries_with_counts, key=lambda x: x['recipe_count'], reverse=True)

    context = {
        "countries": [country['country_of_origin'] for country in sorted_countries],
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))

def country_recipes(request, country):
    template = loader.get_template("polls/recipeList.html")

    # Sort recipes alphabetically
    sorted_recipes = sorted(Recipe.objects.filter(country_of_origin=country), key=lambda x: x.name)
    
    context = {
        "recipes": sorted_recipes,
    }

    return HttpResponse(template.render(context, request))

def recipe_detail(request, id):
    template = loader.get_template("polls/recipeDetail.html")

    recipe = Recipe.objects.get(id=id)

    #  Convert ingredients from string to list
    recipe.ingredients = ast.literal_eval(recipe.ingredients)

    context = {
        "recipe": recipe,
    }

    return HttpResponse(template.render(context, request))

def recipe_list(request):
    template = loader.get_template("polls/recipeList.html")
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified

    # Sort recipes alphabetically
    sorted_recipes = sorted(Recipe.objects.all(), key=lambda x: x.name)

    context = {
        "recipes": sorted_recipes,
    }

    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template("polls/searchResults.html")

    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    query_string = request.GET.get('query')
    
    recipes = Recipe.objects.filter(Q(name__icontains=query_string))

    context = {
        "recipes": get_sorted_recipes(recipes, order_by),
        "query": query_string,
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))


def get_sorted_recipes(recipes, order_by):
    if order_by == 'alphabetical':
        return recipes.order_by('-name')
        
    elif order_by == 'popularity':
        return recipes.annotate(recipe_count=Count('id')).order_by('-recipe_count')
    
    return None
     

