from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Q
from .models import Recipe, Country
import ast

# Create your views here.´

def index(request):
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    template = loader.get_template("homePage.html")

    context = {
        "countries": get_all_sorted_countries(order_by),
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))

def search_recipes_page(request):
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    template = loader.get_template("search/searchRecipes.html")

    search_results = get_searched_recipes(request)

    context = {
        "recipes": get_sorted_recipes(search_results["recipes"], order_by),
        "countries": get_all_sorted_countries(order_by),
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))

def search_by_country_page(request):
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    template = loader.get_template("search/searchByCountry.html")

    search_results = get_searched_recipes(request)

    context = {
        "recipes": get_sorted_recipes(search_results["recipes"], order_by),
        "countries": get_all_sorted_countries(order_by),
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))

def search_by_ingredient_page(request):
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified
    template = loader.get_template("search/searchByIngredient.html")

    search_results = get_searched_recipes(request)

    context = {
        "recipes": get_sorted_recipes(search_results["recipes"], order_by),
        "countries": get_all_sorted_countries(order_by),
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template("search/searchResults.html")
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified

    search_results = get_searched_recipes(request)
    
    context = {
        "recipes": get_sorted_recipes(search_results["recipes"], order_by),
        "name": search_results["name"],
        "country_of_origin": search_results["country_of_origin"],
        "ingredient": search_results["ingredient"],
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

    # Get country info
    country = Country.objects.get(name=recipe.country_of_origin)

    context = {
        "recipe": recipe,
        "country": country
    }

    return HttpResponse(template.render(context, request))

def recipe_list(request):
    template = loader.get_template("recipeList.html")
    order_by = request.GET.get('order', 'popularity')  # Default to popularity if no order is specified

    context = {
        "recipes": get_sorted_recipes(Recipe.objects.all(), order_by),
        "order_by": order_by,
    }

    return HttpResponse(template.render(context, request))

def get_searched_recipes(request):
    recipes = Recipe.objects.all()
    
    # Simple search
    name = request.GET.get('name')
    if name is not None:
        recipes = Recipe.objects.filter(Q(name__icontains=name))

    # Search by country of origin
    country_of_origin = request.GET.get('country_of_origin')
    if country_of_origin is not None:
        recipes = Recipe.objects.filter(Q(country_of_origin__icontains=country_of_origin))

    # Search by ingredient
    ingredient = request.GET.get('ingredient')
    if ingredient is not None:
        recipes = Recipe.objects.filter(Q(ingredients__icontains=ingredient))

    return {
        "recipes": recipes,
        "name": name,
        "country_of_origin": country_of_origin,
        "ingredient": ingredient,
    }

def get_sorted_recipes(recipes, order_by):
    if order_by == 'alphabetical':
        return sorted(recipes, key=lambda recipe: recipe.name)
        
    elif order_by == 'popularity':
        return recipes.annotate(recipe_count=Count('id')).order_by('-recipe_count')
    
    return None

def get_all_sorted_countries(order_by):
    if order_by == 'alphabetical':
        return sorted(Country.objects.all(), key=lambda country: country.name)
        
    elif order_by == 'popularity':
        # Query to get the count of recipes for each country
        countries_with_counts = Recipe.objects.values('country_of_origin').annotate(recipe_count=Count('id'))

        # Sort countries in descending order based on recipe count
        sorted_countries = sorted(countries_with_counts, key=lambda country: country['recipe_count'], reverse=True)
        return set([Country.objects.get(name=country["country_of_origin"]) for country in sorted_countries])

    return None

