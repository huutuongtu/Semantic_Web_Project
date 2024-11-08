import pandas as pd
from utils import get_individual_from_title, category_mapping, remove_special_chars_keep_punct_space
import ast
from owlready2 import *
from owlready2.sparql.endpoint import *

# Load one or more ontologies
go = get_ontology("./misc/ontology_with_data.owl").load()

base_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"""

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
        
        return list(default_world.sparql(base_query + query))
        # return query
    else:
        return False

def get_book_from_publisher(publisher: str):

    query = """

  SELECT ?title ?author ?publisher
  WHERE {
     ?publisher_entity :publisherHasName "%s" .
     ?publisher_entity :isPublisherOf ?book .
     ?publisher_entity :publisherHasName ?publisher .
     ?book :hasAuthor ?author_entity .
     ?author_entity :hasName ?author .
     ?book :hasTitle ?title .
  }
  """ % (publisher)
    
    query = """

  SELECT ?title ?author ?publisher
  WHERE {
     ?publisher_entity :publisherHasName "%s" .
     ?book :hasPublisher ?publisher_entity .
     ?publisher_entity :publisherHasName ?publisher .
     ?book :hasAuthor ?author_entity .
     ?author_entity :hasName ?author .
     ?book :hasTitle ?title .
  }
  """ % (publisher)
    # print(base_query + query)

    return list(default_world.sparql(base_query + query))


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
    return list(default_world.sparql(base_query + query))

def get_book_from_author(author: str):
    """This return book individual and title of book
    """
    query = """

    SELECT ?booktitle ?bookauthor ?bookpublisher
        WHERE {
                ?author :hasName "%s" .
                ?book :hasAuthor ?author .
                ?book :hasTitle ?booktitle .
                ?author :hasName ?bookauthor .
                ?book :hasPublisher ?publisher_individual .
                ?publisher_individual :publisherHasName ?bookpublisher .
                }
            """ % (str(author))
    # print(query)
    return list(default_world.sparql(base_query + query))


def get_book_from_pre_infomation(infomation: dict):
    try:
        res = []
        query = """

    SELECT ?booktitle ?author ?publisher ?numberpage
            WHERE { \n
        """
        if infomation['title']:
            bookTitle = remove_special_chars_keep_punct_space(infomation['title'])
            query += '''?book :hasTitle "%s" \n
            ''' %(str(bookTitle))
        if infomation['category']:
            category = infomation['category']
            if category in category_mapping().keys():
                query += '''?book rdf:type :%s \n
                ''' %(str(category))
        if infomation['author']:
            author = infomation['author']
            query += '''?entity_author :hasName "%s" .
            ''' %(str(author))
        if infomation['language']:
            language = infomation['language']
            query += '''?book :hasLanguage :%s \n
            ''' %(str(language))
        if infomation['pages']:
            pages = infomation['pages']
        
            
        query += '?book :hasTitle ?booktitle \n'
        query += '?book :hasAuthor ?entity_author \n'
        query += '?book :hasPublisher ?entity_publisher \n'
        query += '?entity_author :hasName ?author \n'
        query += '?entity_publisher :publisherHasName ?publisher \n'
        query += '''?book :hasNumberPage ?numberpage .                
            }
                
            '''
        all_individual = list(default_world.sparql(base_query + query))
        for individual in all_individual:
            if pages-20 <= individual[3] <= pages+20:
                res.append(individual)
        return res
    except:
        return []
    
#keys should be False if no data
# info = {"category": "Fantasy", "pages": 300, "language": 'English', "author": 'Stephanie Garber', "title": False}
# print(get_book_from_pre_infomation(info))



# print(list(default_world.sparql_query(base_query + get_book_from_publisher("Routledge"))))
# print(list(default_world.sparql_query(base_query + get_book_from_author("Aaron Erickson Erickson"))))
#[['The Nomadic Developer Surviving and Thriving in the World of Technology Consulting', 'Aaron Erickson Erickson', 'Addison-Wesley']]