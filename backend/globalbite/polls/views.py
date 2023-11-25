from django.http import HttpResponse
from django.template import loader
from .models import Recipe

# Create your views here.´

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def recipe_list(request):
    template = loader.get_template("polls/recipes.html")
    context = {
        "recipes": Recipe.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def country_list(request):
    template = loader.get_template("polls/countries.html")
    context = {
        "countries": Recipe.objects.values_list('country_of_origin', flat=True).distinct().order_by('country_of_origin'),
    }
    return HttpResponse(template.render(context, request))

def country_recipes(request, country):
    template = loader.get_template("polls/recipes.html")
    context = {
        "recipes": Recipe.objects.filter(country_of_origin=country),
    }
    return HttpResponse(template.render(context, request))