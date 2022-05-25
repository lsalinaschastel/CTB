
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from statistics import mode
from pptx import Presentation




# def test_datos (file1, file2):
from pptx.util import Inches

df = pd.read_csv('COVID19_data.csv', index_col=0)
dictio = pd.read_csv('Dict.csv', delimiter=';')


cat_vars = []
num_vars = []

# Create ppt
ppt = Presentation()
blank_slide_layout = ppt.slide_layouts[6]
slide = ppt.slides.add_slide(blank_slide_layout)
left = top = Inches(1)

for i, row in dictio.iterrows():
    if dictio['Type'][i] == 'Num':
        num_vars.append(dictio['Variable'][i])
    else:
        cat_vars.append(dictio['Variable'][i])

df_cat = df[cat_vars]
df_num = df[num_vars]


# Analysis of categorical variables


for i in df_cat.columns:
    # Null values y percentage
    print("Number of missing values in attribute " + str(i) + ' is:', df_cat[i].isnull().sum(), "which is a" , round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100) , 2) , "%" )

    if len(df_cat[i].value_counts()) <= 2:
        fig = plt.figure(figsize=(20, 5))
        df_cat.groupby(i).size().plot(kind='pie', textprops={'fontsize': 20},
                                          colors=['gold', 'blue'])

        plt.savefig("Piechart_variable_" + str(i), dpi=300)

        # Pasar las fotos a ppt
        img_path = "Piechart_variable_" + str(i) + '.png'
        slide=ppt.slides.add_slide(blank_slide_layout)
        pic = slide.shapes.add_picture(img_path,
                                       left, top)
        left = Inches(1)
        height = Inches(1)


    else:
        #Bar chart
        print("bar chart")

ppt.save("Test.pptx")



