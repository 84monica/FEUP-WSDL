from django.http import HttpResponse
from django.template import loader
from .models import Recipe

# Create your views here.´

def index(request):
    template = loader.get_template("polls/index.html")
    context = {
        "recipes": Recipe.objects.all(),
    }
    return HttpResponse(template.render(context, request))