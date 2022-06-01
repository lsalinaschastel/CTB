
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from statistics import mode
from pptx import Presentation
from pptx.util import Inches



# Test data
#df = pd.read_csv('COVID19_data.csv', index_col=0)
#dictio = pd.read_csv('Dict.csv', delimiter=';')

# Real data
df = pd. read_excel('Final_data.xlsx', index_col=None, na_values=['NA'])
dictio=pd. read_excel('Dict_3.xlsx', index_col=None) # or 0

# Remove date columns (if it does not say in the type it is a date)
# for i in df.columns:
#     if df[i].dtype=='datetime64[ns]':
#         df=df.drop([i],axis=1)
#         dictio=dictio.drop([i])


# Create ppt
ppt = Presentation()

# Remove columns that have no values



# Separate cat from numerical variables
cat_vars = []
num_vars = []
for i, row in dictio.iterrows():
    if dictio['Type'][i] == 'num':
        num_vars.append(dictio['Variable'][i])
    elif dictio['Type'][i] == 'cat':
        cat_vars.append(dictio['Variable'][i])
        # cat_vars.append(dictio.index[i])


df_cat = df[cat_vars]
df_num = df[num_vars]


# Analysis of CATEGORICAL variables
# si están todas las columnas vacías quitar datos.

for i in df_cat.columns:

    if len(df_cat[i].value_counts()) <= 2:
        # Pie chart
        fig = plt.figure(figsize=(20, 5))
        df_cat.groupby(i).size().plot(kind='pie', textprops={'fontsize': 15},
                                      colors=['gold', 'blue'], autopct=lambda x: str(round(x, 2)) + '%',
                                      pctdistance=0.5)

        #plt.legend(loc="lower left")
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
        subtitle.text = str(len(df_cat[i].value_counts())) + " categories" + "\nSample size: " + str(len(df_cat)) + "\nMissing values: " + str(df_cat[i].isnull().sum()) + " (" + str(round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100),2)) + " %)" + "\nMode: " + str(statistics.mode(df_cat[i]))

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
            round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100), 2)) + " %)" + "\nMode: " + str(statistics.mode(df_cat[i]))




# Analysis of QUANTITATIVE variables

for i in df_num.columns:
    # Statistics (appear directly in subtitle)
    #means.append(np.nanmean(df_num[i]))
    #medians.append(np.nanmedian(df_num[i]))
    #modes.append(statistics.mode(df_num[i]))

    # Box plot
    fig = plt.figure()
    plt.subplot(1,2,1)
    df_num[i].plot.box(fontsize=8)
    plt.title("Box plot")
    #plt.savefig("Boxplot_variable_" + str(i), dpi=300)

    # Finding outliers
    outlier_free_list = []
    outliers = []
    perc_outliers = []
    Q3 = np.nanquantile(df_num[i], 0.75)
    Q1 = np.nanquantile(df_num[i], 0.25)

    IQR = Q3 - Q1

    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR

    # Filter the data that are free of outliers
    for x in df_num[i]:
        if (x > lower_range) & (x < upper_range):
            outlier_free_list.append(x)

        else:
            outliers.append(x)
    perc_outliers.append((len(outliers) / len(df_num)) * 100)


    # Histogram

    plt.subplot(1, 2, 2)
    sns.distplot(df_num[i]) #scatter plot
    plt.title('Distribution')
    plt.ylabel("")
    plt.savefig("Num_variable_" + str(i), dpi=300)

    # Picts to ppt
    img_path = "Num_variable_" + str(i) + '.png'
    #img_path2 = "Hist_variable_" + str(i) + '.png'

    graph_slide_layout = ppt.slide_layouts[8]
    slide = ppt.slides.add_slide(graph_slide_layout)

    title = slide.shapes.title
    title.text = str(i)
    placeholder = slide.placeholders[1]
    pic = placeholder.insert_picture(img_path)
    subtitle = slide.placeholders[2]
    subtitle.text = "Variable " + str(i) + " has: " + str(len(outliers)) + " outliers" + "\nMean: " + str(round(np.nanmean(df_num[i]),2)) + "\nMedian: " + str(np.nanmedian(df_num[i]))

ppt.save("Test.pptx")

