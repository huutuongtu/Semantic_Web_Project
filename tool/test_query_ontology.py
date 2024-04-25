import flask

from owlready2 import *
from owlready2.sparql.endpoint import *
import rdflib

# Load one or more ontologies
go = get_ontology("./ontology_with_data.owl").load()

base_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"""

#query all data has type fantasy
query = """
           SELECT ?book ?title ?author
                WHERE {
                        ?book rdf:type :Fantasy .
                        ?book :hasAuthor ?author .
                        ?book :hasTitle ?title .
                        }
    """
print(list(default_world.sparql(base_query + query)))

#query all data type book
query = """
        SELECT ?item ?title ?author
            WHERE {
            { 
                ?item rdf:type :Book. 
            }
            UNION
            { 
                ?item rdf:type ?childClass .
                ?childClass rdfs:subClassOf* :Book .
                ?item :hasAuthor ?author .
                ?item :hasTitle ?title .
            }
            }
"""

print(list(default_world.sparql(base_query + query)))
