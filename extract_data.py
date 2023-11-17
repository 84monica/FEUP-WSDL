from SPARQLWrapper import SPARQLWrapper, JSON

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

        for r in ret["results"]["bindings"]:
            print(r)

    except Exception as e:
        print(e)

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
        print("Dish Name:" + result["name"]["value"] + "\t Country of Origin: "  + result["countryLabel"]["value"])


foodDB()
dbpedia()
