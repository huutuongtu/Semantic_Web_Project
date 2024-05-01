import pandas as pd
from utils import get_individual_from_title, category_mapping, remove_special_chars_keep_punct_space
import ast
from owlready2 import *
from owlready2.sparql.endpoint import *

# Load one or more ontologies
go = get_ontology("./misc/ontology_with_data.owl").load()

# base_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#         PREFIX owl: <http://www.w3.org/2002/07/owl#>
#         PREFIX : <http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#>
#         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"""

def get_book_from_category(category: str):
    """Return list book individual, title and author belong to category
    """
    if go.search_one(iri = "http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#" + category):
        query = """

                SELECT  ?title ?author ?publisher
                        WHERE {
                                ?book rdf:type :%s .
                                OPTIONAL {?book :hasTitle ?title}
                                OPTIONAL {?book :hasAuthor ?author_individual}
                                OPTIONAL {?author_individual :hasName ?author}
                                OPTIONAL {?book :hasPublisher ?publisher_individual}
                                OPTIONAL {?publisher_individual :publisherHasName ?publisher}
                                }
            """ % (category)
        
        return query
    else:
        return False

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
    
    return query

def get_author_from_book(bookTitle: str):
    """This return list author individual and author name isAuthorOf Book
    """
    bookTitle = remove_special_chars_keep_punct_space(bookTitle)
    query = """

            SELECT ?booktitle ?author ?publisher
                    WHERE {
                            ?book :hasTitle "%s" .
                            OPTIONAL {?book :hasAuthor ?author_individual} .
                            OPTIONAL {?author_individual :hasName ?author} .
                            OPTIONAL {?book :hasTitle ?booktitle} .
                            OPTIONAL {?book :hasPublisher ?publisherin} .
                            OPTIONAL {?publisherin :publisherHasName ?publisher} .
                            }
        """ % (str(bookTitle))
    return query

def get_book_from_author(author: str):
    """This return book individual and title of book
    """
    query = """

                SELECT ?booktitle ?bookauthor ?bookpublisher
                    WHERE {
                            ?author :hasName "%s" .
                            ?author :isAuthorOf ?book .
                            ?book :hasTitle ?booktitle .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher_individual .
                            ?publisher_individual :publisherHasName ?bookpublisher .
                            }
        """ % (str(author))
    print(query)
    return query



# print(get_book_from_category("Fantasy")) #should merge same book individual
# print(get_author_from_book("Video Games and Culture")) #return list author
# print(get_book_same_author_as("Video Games and Culture")) #return list book that has the same author
# print(get_book_from_author('Daniel Muriel')) #return isAuthorOf => Book  