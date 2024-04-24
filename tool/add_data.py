import pandas as pd
from utils import get_individual_from_title 


#create a dictionary save language author and publisher
hasLanguage = {}
hasAuthor = {}
hasPublisher = {}

data = pd.read_csv("./data.csv")
for i in range(len(data)):
    hasLanguage[data['hasLanguage'][i]] = False
    hasAuthor[get_individual_from_title(data['hasAuthor'][i])] = False
    hasPublisher[get_individual_from_title(data['hasPublisher'][i])] = False

#this will save syntax info of author, language, publisher owl 
_need_to_append = ''
#this will save syntax info of book owl
_book_to_append = ''

for i in range(len(data)):

    #for author
    nameAuthorIndividual = data['hasAuthor'][i]
    authorIndividual = get_individual_from_title(nameAuthorIndividual)
    if not hasAuthor[authorIndividual]: 
        author_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
    <ClassAssertion>
        <Class IRI="#Author"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
    <DataPropertyAssertion>
        <DataProperty IRI="#hasName"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
        """ % (authorIndividual, authorIndividual, authorIndividual, nameAuthorIndividual)
        hasAuthor[authorIndividual] = True
        _need_to_append += author_str

    #for language
    languageIndividual = data['hasLanguage'][i]
    if not hasLanguage[languageIndividual]: 
        language_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
    <ClassAssertion>
        <Class IRI="#Language"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
        """ % (languageIndividual, languageIndividual)
        hasLanguage[languageIndividual] = True
        _need_to_append += language_str

    #for publisher
    namePublisherIndividual = data['hasPublisher'][i]
    publisherIndividual = get_individual_from_title(namePublisherIndividual)
    if not hasPublisher[publisherIndividual]: 
        publisher_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
    <ClassAssertion>
        <Class IRI="#Publisher"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
    <DataPropertyAssertion>
        <DataProperty IRI="#publisherHasName"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
        """ % (publisherIndividual, publisherIndividual, publisherIndividual, namePublisherIndividual)
        hasPublisher[publisherIndividual] = True  
        _need_to_append += publisher_str 
 
    bookTitle = data['hasTitle'][i]
    bookIndividual = get_individual_from_title(data['hasTitle'][i])
    bookId = data['hasID'][i]
    bookNumberPage = data['hasNumberPage'][i]
    bookPublicYear = data['hasPublicYear'][i]
    bookExtension = data['hasExtension'][i]
    bookSize = data['hasSize'][i]
    bookAuthor = get_individual_from_title(data['hasAuthor'][i])
    bookPublisher = get_individual_from_title(data['hasPublisher'][i])
    bookLanguage = data['hasLanguage'][i]
    bookRate = data['hasRate'][i]
    bookTags = data['hasTags'][i]
    bookCategory = data['hasCategory'][i].split(",")
    
    #create individual
    book_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
            """ %(bookIndividual)
    #add category
    for category in bookCategory:
        category = category.strip()
        book_str_1 = """
    <ClassAssertion>
        <Class IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
            """ % (category, bookIndividual)
        book_str += book_str_1
    
    book_str_2 = """

    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#hasAuthor"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>

    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#hasLanguage"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>

    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#hasPublisher"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasExtension"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&rdf;PlainLiteral">%s</Literal>
    </DataPropertyAssertion>
    
    <DataPropertyAssertion>
        <DataProperty IRI="#hasID"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;int">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasNumberPage"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;int">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasPublishYear"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;int">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasSize"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
    
    <DataPropertyAssertion>
        <DataProperty IRI="#hasTittle"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasTag"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
        """ % (bookIndividual, bookAuthor, bookIndividual, bookLanguage, bookIndividual, bookPublisher, bookIndividual, bookExtension, bookIndividual, bookId, bookIndividual, bookNumberPage, bookIndividual, bookPublicYear, bookIndividual, bookSize, bookIndividual, bookTitle, bookIndividual, bookTags)
    book_str += book_str_2
    _book_to_append += book_str

data_to_append = _need_to_append + _book_to_append
f = open("./ontology_wo_data.owl", "r", encoding='utf8').read()
new_f = f.split("</Ontology>")
data_update = new_f[0] + "\n" + data_to_append + "</Ontology>"  + new_f[1]
save_path = 'ontology_with_data.owl'

with open(save_path, 'w', encoding='utf8') as owl_file:
    owl_file.write(data_update)
