
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from statistics import mode
from pptx import Presentation
from pptx.util import Inches


df = pd.read_csv('COVID19_data.csv', index_col=0)
dictio = pd.read_csv('Dict.csv', delimiter=';')


cat_vars = []
num_vars = []

# Create ppt
ppt = Presentation()
#blank_slide_layout = ppt.slide_layouts[6]
#slide = ppt.slides.add_slide(blank_slide_layout)
#left = top = Inches(1)

for i, row in dictio.iterrows():
    if dictio['Type'][i] == 'Num':
        num_vars.append(dictio['Variable'][i])
    else:
        cat_vars.append(dictio['Variable'][i])

df_cat = df[cat_vars]
df_num = df[num_vars]


# Analysis of CATEGORICAL variables


for i in df_cat.columns:

    if len(df_cat[i].value_counts()) <= 2:
        # Pie chart
        fig = plt.figure(figsize=(20, 5))
        df_cat.groupby(i).size().plot(kind='pie', textprops={'fontsize': 15},
                                      colors=['gold', 'blue'], autopct=lambda x: str(round(x, 2)) + '%',
                                      pctdistance=0.5)

        #plt.legend(loc="lower left")
        #plt.title("Distribution")
        plt.ylabel("")
        plt.savefig("Piechart_variable_" + str(i), dpi=300)

        # Pict to ppt
        img_path = "Piechart_variable_" + str(i) + '.png'

        graph_slide_layout = ppt.slide_layouts[8]
        slide = ppt.slides.add_slide(graph_slide_layout)

        title = slide.shapes.title
        title.text = str(i)
        placeholder = slide.placeholders[1]
        pic = placeholder.insert_picture(img_path)
        subtitle = slide.placeholders[2]
        subtitle.text = str(len(df_cat[i].value_counts()))+ " categories" + "\nSample size: " + str(len(df_cat)) + "\nMissing values: " + str(df_cat[i].isnull().sum()) + " (" + str(round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100),2)) + " %)"

    else:
        # Bar chart
        fig = plt.figure()
        df_cat.groupby(i).size().plot(kind='bar', rot=0)
        plt.savefig("Barchart_variable_" + str(i), dpi=300)

        # Pict to ppt
        img_path = "Barchart_variable_" + str(i) + '.png'
        graph_slide_layout = ppt.slide_layouts[8]
        slide = ppt.slides.add_slide(graph_slide_layout)
        title = slide.shapes.title
        title.text = str(i)
        placeholder = slide.placeholders[1]
        pic = placeholder.insert_picture(img_path)
        subtitle = slide.placeholders[2]
        subtitle.text = str(len(df_cat[i].value_counts())) + " categories" + "\nSample size: " + str(
            len(df_cat)) + "\nMissing values: " + str(df_cat[i].isnull().sum()) + " (" + str(
            round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100), 2)) + " %)"




# Analysis of QUANTITATIVE variables
for i in df_cat.columns:

ppt.save("Test.pptx")

