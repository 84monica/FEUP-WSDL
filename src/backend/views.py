from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Q
from .models import Recipe, Country
import ast

# Create your views here.´

def index(request):
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    template = loader.get_template("homePage.html")

    if order_by == 'alphabetical':
        sorted_countries = sorted(Country.objects.all(), key=lambda country: country.name)
        
    elif order_by == 'popularity':
        # Query to get the count of recipes for each country
        countries_with_counts = Recipe.objects.values('country_of_origin').annotate(recipe_count=Count('id'))

        # Sort countries in descending order based on recipe count
        sorted_countries = sorted(countries_with_counts, key=lambda country: country['recipe_count'], reverse=True)
        sorted_countries = set([Country.objects.get(name=country["country_of_origin"]) for country in sorted_countries])

    context = {
        "countries": sorted_countries,
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))

def country_recipes(request, country):
    template = loader.get_template("recipeList.html")

    # Sort recipes alphabetically
    sorted_recipes = sorted(Recipe.objects.filter(country_of_origin=country), key=lambda x: x.name)

    context = {
        "recipes": sorted_recipes,
    }

    return HttpResponse(template.render(context, request))

def recipe_detail(request, id):
    template = loader.get_template("recipeDetail.html")

    recipe = Recipe.objects.get(id=id)

    #  Convert ingredients from string to list
    recipe.ingredients = ast.literal_eval(recipe.ingredients)

    context = {
        "recipe": recipe,
    }

    return HttpResponse(template.render(context, request))

def recipe_list(request):
    template = loader.get_template("recipeList.html")
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified

    # Sort recipes alphabetically
    sorted_recipes = sorted(Recipe.objects.all(), key=lambda x: x.name)

    context = {
        "recipes": sorted_recipes,
    }

    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template("searchResults.html")

    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    name = request.GET.get('name')
    if name is not None:
        recipes = Recipe.objects.filter(Q(name__icontains=name))

    # Advanced search
    country_of_origin = request.GET.get('country_of_origin')
    abstract = request.GET.get('details')

    if country_of_origin is not None:
        recipes = Recipe.objects.filter(Q(country_of_origin__icontains=country_of_origin))

    if abstract is not None:
        recipes = Recipe.objects.filter(Q(abstract__icontains=abstract))
    

    context = {
        "recipes": get_sorted_recipes(recipes, order_by),
        "name": name,
        "country_of_origin": country_of_origin,
        "abstract": abstract,
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))


def get_sorted_recipes(recipes, order_by):
    if order_by == 'alphabetical':
        return recipes.order_by('-name')
        
    elif order_by == 'popularity':
        return recipes.annotate(recipe_count=Count('id')).order_by('-recipe_count')
    
    return None
     

