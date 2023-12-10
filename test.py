from owlready2 import *
from SPARQLWrapper import SPARQLWrapper, JSON
from django.core.management.base import BaseCommand

def foodDB():
    onto = get_ontology("http://purl.org/heals/food")
    onto2 = get_ontology("http://purl.org/heals/ingredient")
    onto2.load()
    onto.load()

    query = list(default_world.sparql("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns>
    SELECT ?recipe
    WHERE {
        ?recipe rdf:type food:Food.
    }"""))

    print(query.count)
    print(query[0])
    print(query)


def dbpedia():
    # Query for all dishes and their country of origin

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?name ?thumbnail ?countryLabel ?countryThumbnail (GROUP_CONCAT(?ingredientLabel; SEPARATOR=", ") AS ?ingredients) ?abstract
        WHERE {
            ?dish rdf:type dbo:Food ;
                rdfs:label ?name ;
                dbo:country ?country;
                dbo:ingredient ?ingredient;
                dbo:abstract ?abstract;
                dbo:thumbnail ?thumbnail.
            ?country a dbo:Country;
                rdfs:label ?countryLabel;
                dbo:thumbnail ?countryThumbnail.
            ?ingredient rdfs:label ?ingredientLabel.
            FILTER(LANG(?name) = "en")
            FILTER(LANG(?countryLabel) = "en")
            FILTER(LANG(?ingredientLabel) = "en")
            FILTER(LANG(?abstract) = "en")
        } GROUP BY ?dish ?name ?thumbnail ?countryLabel ?countryThumbnail ?abstract 
        LIMIT 10
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    countries = set([result["countryThumbnail"]["value"] for result in results["results"]["bindings"]])
    print(countries)

dbpedia()