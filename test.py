from owlready2 import *

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

foodDB()