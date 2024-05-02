import pandas as pd
from utils import get_individual_from_title, category_mapping, remove_special_chars_keep_punct_space
import ast
from owlready2 import *
from owlready2.sparql.endpoint import *

# Load one or more ontologies
go = get_ontology("./ontology_with_data.owl").load()

base_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"""

def get_book_from_category(category: str):
    """Return list book individual, title and author belong to category
    """
    query = """
            SELECT ?book ?title ?author
                    WHERE {
                            ?book rdf:type :%s .
                            OPTIONAL {?book :hasTitle ?title}
                            OPTIONAL {?book :hasAuthor ?author_individual}
                            OPTIONAL {?author_individual :hasName ?author}
                            }
        """ % (category)
    
    res = default_world.sparql_query(base_query + query)
    return list(res)

def get_author_from_book(bookTitle: str):
    """This return list author individual and author name isAuthorOf Book
    """
    bookTitle = remove_special_chars_keep_punct_space(bookTitle)
    query = """
            SELECT ?author_individual ?author
                    WHERE {
                            ?book :hasTitle "%s" .
                            ?book :hasAuthor ?author_individual .
                            ?author_individual :hasName ?author .
                            }
        """ % (str(bookTitle))
    res = default_world.sparql_query(base_query + query)
    return list(res)

def get_book_from_author(author: str):
    """This return book individual and title of book
    """
    query = """
            SELECT ?book ?booktitle
                    WHERE {
                            ?author :hasName "%s" .
                            ?author :isAuthorOf ?book .
                            ?book :hasTitle ?booktitle .
                            }
        """ % (str(author))
    res = default_world.sparql_query(base_query + query)
    
    return list(res)

def get_book_from_publisher(publisher: str):

    query = """
            SELECT  ?title ?author ?publisher
                    WHERE {
                            ?individual_publisher :publisherHasName "%s" .
                            ?individual_publisher :publisherHasName ?publisher .
                            OPTIONAL {?individual_publisher :isPublisherOf ?inbook}
                            OPTIONAL {?inbook :hasAuthor ?author_individual}
                            OPTIONAL {?author_individual :hasName ?author}
                            OPTIONAL {?inbook :hasTitle ?title}
                            }
        """ % (publisher)
    res = default_world.sparql_query(base_query + query)
    
    return list(res)

# print(get_book_from_publisher("4th Estate AU"))


query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                SELECT ?booktitle ?bookauthor ?bookpublisher
                    WHERE {
                            ?author :hasName "Michel Broué" .
                            ?author :isAuthorOf ?book .
                            ?book :hasTitle ?booktitle .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher_individual .
                            ?publisher_individual :publisherHasName ?bookpublisher .
                            }

                            """

print(list(default_world.sparql_query(query)))
# def get_book_same_author_as(bookTitle: str):
#     list_author = get_author_from_book(bookTitle=bookTitle)
#     list_author_individual = []
#     for i in range(len(list_author)):
#         list_author_individual.append(list_author[i][0])
#         print(list_author[i][0])
#     for author_individual in list_author_individual:

#         query = """
#                 SELECT ?book ?listbook
#                         WHERE {
#                                 ?book :hasAuthor ?author_individual .
#                                 ?author_individual :isAuthorOf :listbook .
#                                 }
#             """
#         bindings = {"?author_individual": author_individual}
# #     print(query)
#         res = default_world.sparql_query(base_query + query, bindings = bindings)
#         print(list(res))
#     return list(res)


# print(get_book_from_category("Fantasy")) #should merge same book individual
# print(get_author_from_book("Video Games and Culture")) #return list author
# print(get_book_same_author_as("Video Games and Culture")) #return list book that has the same author
# print(get_book_from_author('Daniel Muriel')) #return isAuthorOf => Book  