# Author: Isuru Kalhara
# Reference : https://pythonspot.com/flask-web-forms/

import os
import sys

from jiwer import cer
import pyparsing
import rdflib
from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, validators
from owlready2 import *
from owlready2.sparql.endpoint import *
from query_api import get_book_from_category, get_author_from_book, get_book_from_author, get_book_from_publisher
from owlready2 import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
global no_query
no_query = True
global anything


class ReusableForm(Form):
    query = StringField('Query:', validators=[validators.data_required()])
    query_category = False
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        global graph
        form = ReusableForm(request.form)
        if form.errors:
            print(form.errors)

        base_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"""

        output = {}
        query = ''

        if request.method == 'POST':

            if(request.form['but1']=='Business'):
                no_query = True
                #car price mpg year seat
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Business .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """

            elif(request.form['but1']=='Computer'):
                no_query = True
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Computer .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """

            elif(request.form['but1']=='Economy'):
                no_query = True
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Economy .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """

            elif(request.form['but1']=='Literature'):
                no_query = True
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Literature .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """

            elif(request.form['but1']=='Math'):
                no_query = True
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Math .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """

            elif(request.form['but1']=='Medicine'):
                no_query = True
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Medicine .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """
            elif(request.form['but1']=='Psychology'):
                no_query = True
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Psychology .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """

            elif(request.form['but1']=='AllBook'):
                no_query = True
                query = """
                    SELECT ?bookname ?bookauthor ?bookpublisher
                        WHERE {
                            ?book rdf:type ?childClass .
                            ?childClass rdfs:subClassOf* :Book .
                            ?book :hasTitle ?bookname .
                            ?book :hasAuthor ?author .
                            ?author :hasName ?bookauthor .
                            ?book :hasPublisher ?publisher .
                            ?publisher :publisherHasName ?bookpublisher .
                        }

            """
            
            else:
                anything = request.form['query']
                no_query = False
                if anything == "":
                    data = []
                else:
                    book_from_category = get_book_from_category(anything)
                    author_from_book = get_author_from_book(anything)
                    book_from_author = get_book_from_author(anything)
                    book_from_publisher = get_book_from_publisher(anything)
                    # print(book_from_category)
                    try:
                        print(1)
                        print(book_from_category)
                        data = list(default_world.sparql(base_query + book_from_category))
                    except:
                        try:
                            print(2)
                            print(book_from_author)
                            data = list(default_world.sparql(base_query + book_from_author))
                        except:
                            try:
                                print(3)
                                print(author_from_book)
                                data = list(default_world.sparql(base_query + author_from_book))
                            except:
                                try:
                                    print(4) 
                                    data = list(default_world.sparql(base_query + book_from_publisher))
                                except:
                                    print("dkm")  
            
            cols = ["Book", "Author", "Publisher"]
            if no_query is False:
                if data is None:
                    data = ["", "", ""]
                print(data)
            else:
                query = base_query + query
                data = list(default_world.sparql(base_query + query))
                print(data)

                    

            output = {'columns': cols,
                      'data': data}
            flash('Results ready!')
        # except pyparsing.ParseException:
        #     print("ERROR: query entered...\n", query)
        #     flash('Error: Invald Query')

        return render_template('home.html', form=form, title="Book Search", output=output)


if __name__ == "__main__":

    go = get_ontology("./misc/ontology_with_data.owl").load()
    app.run(debug=True)
