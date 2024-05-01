import pandas as pd
from utils import get_individual_from_title
import ast
data = pd.read_csv("./data.csv")
classes = []

for i in range(len(data)):
    classes.append(data["hasCategory"][i])
classes = list(set(classes))

mapping_category = {}
for classs in classes:
    mapping_category[classs] = classs
mapping_category['Optimization. Operations Research'] = 'Optimization'
mapping_category ['Popular scientific literature'] = 'PopularScientificLiterature'
mapping_category['Operating Systems'] = 'OperatingSystem'
mapping_category['Mathematical Economics'] = 'MathematicalEconomics'
mapping_category['Love, erotic'] = 'LoveErotic'
mapping_category['Databases'] = 'Database'
mapping_category['Creative Thinking'] = 'CreativeThink'


def category_mapping():
    return mapping_category


#2 language russian, english
# special &
# language Russian (Old) ??!
# Spanish; Quechua 
# Рецепт хорошего сна.
