import pandas as pd
from utils import get_individual_from_title
import ast

data = pd.read_csv("./data.csv")

author_book = {}
set_author = []
for i in range(len(data)):
    xyz = data['hasAuthor'][i]
    for author in ast.literal_eval(xyz):
        set_author.append(author)
        author_book[author]=0

for i in range(len(data)):
    xyz = data['hasAuthor'][i]
    for author in ast.literal_eval(xyz):
        author_book[author]+=1

for i in range(len(data)):
    xyz = data['hasAuthor'][i]
    for author in ast.literal_eval(xyz):
        if author_book[author]>5:
            print(author)
            print(author_book[author])
