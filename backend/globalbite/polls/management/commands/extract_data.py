# extract_data.py
from SPARQLWrapper import SPARQLWrapper, JSON
from django.core.management.base import BaseCommand
from polls.models import Recipe

class Command(BaseCommand):
    help = 'Populate recipes'

    def handle(self, *args, **options):
        # Delete all recipes before populating
        delete_all()

        # Extract data from DBpedia
        dbpedia()

        self.stdout.write(self.style.SUCCESS('Successfully populated recipes'))

def delete_all():
    # Delete all recipes
    Recipe.objects.all().delete()

def dbpedia():
    # Query for all dishes and their country of origin

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?name ?countryLabel
        WHERE {
            ?dish rdf:type dbo:Food ;
                rdfs:label ?name ;
                dbo:country ?country.
            ?country rdfs:label ?countryLabel.
            FILTER(LANG(?name) = "en")
            FILTER(LANG(?countryLabel) = "en")
        }
        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        Recipe.objects.create(
            name=result["name"]["value"],
            country_of_origin=result["countryLabel"]["value"]
        )

def foodDB():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery("""
        PREFIX food: <http://purl.org/heals/food/>
        PREFIX ingredient: <http://purl.org/heals/ingredient/>
        SELECT DISTINCT ?recipe
        WHERE {
            ?recipe food:hasIngredient ingredient:Beef .
        }
    """)

    try:
        sparql.setReturnFormat(JSON)
        ret = sparql.query().convert()

        # print(ret)

        for r in ret["results"]["bindings"]: # TODO: Write to Models
            print(r)

    except Exception as e:
        print(e)
