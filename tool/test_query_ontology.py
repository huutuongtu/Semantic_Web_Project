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

#query all data has type Fantasy
query = """
           SELECT ?book ?title ?author
                WHERE {
                        ?book rdf:type :Fantasy .
                        OPTIONAL {?book :hasAuthor ?author}
                        OPTIONAL {?book :hasTitle ?title}
                        }
    """
print(list(default_world.sparql(base_query + query)))

#this will return only item type Book not contain item subclass of Book (not like reasoning).
query = """
           SELECT ?book
                WHERE {
                        ?book rdf:type :Book .
                      }
    """
print(list(default_world.sparql(base_query + query)))

#this will return nothing => chuatenhungchiecnhan doesn't have author and title => need add optional like first query
query = """
           SELECT ?book ?title ?author
                WHERE {
                        ?book rdf:type :Book .
                        ?book :hasAuthor ?author .
                        ?book :hasTitle ?title .
                      }
    """
print(list(default_world.sparql(base_query + query)))

#query all data has type book
query = """
        SELECT ?book
            WHERE {
                ?book rdf:type ?childClass .
                ?childClass rdfs:subClassOf* :Book .
            }

"""
print(list(default_world.sparql(base_query + query)))


#Query all book of a author

query = """
        SELECT ?nameauthor ?namebook
            WHERE {
                ?author :hasName "Kameron Hussain" .
                ?book rdf:type ?childClass .
                ?book :hasTitle ?namebook
                ?author :hasName ?nameauthor
                ?childClass rdfs:subClassOf* :Book .
                ?book :hasAuthor ?author
            }

"""

print(list(default_world.sparql(base_query + query)))



#Query all books belong to a publisher with infomation (author and description), if a book not have description => return None in hasDescription

query = """
        SELECT ?title ?name_author ?description
            WHERE {
                ?publisher :publisherHasName "ACT" .
                ?book rdf:type ?childClass .
                ?childClass rdfs:subClassOf* :Book .
                ?book :hasPublisher ?publisher
                ?book :hasTitle ?title .
                ?book :hasAuthor ?author .
                ?author :hasName ?name_author
                OPTIONAL {?book :hasDescription ?description}
            }

"""

print(list(default_world.sparql(base_query + query)))

 