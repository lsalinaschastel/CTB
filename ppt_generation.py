from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from pptx import Presentation



# Import data
df=pd.read_csv('concat_datas_elea.csv', index_col=0, sep=';')
dictio = pd.read_csv('Dict_final.csv', delimiter=';')

# Create ppt
ppt = Presentation()

# Separate cat from numerical variables
cat_vars = []
num_vars = []

for i, row in dictio.iterrows():
    if dictio['Type'][i] == 'num':
        num_vars.append(dictio['Variable'][i])
    elif dictio['Type'][i] == 'cat':
        cat_vars.append(dictio['Variable'][i])
    #elif dictio['Type'][i] == 'date':
        #date_vars.append(dictio['Variable'][i])


df_cat = df[cat_vars]
df_num = df[num_vars]
#df_date = df[date_vars]


# Analysis of DATE VARIABLES

df = df.fillna('Missing values')

# We create new variables that will be the result of operating with the dates
df_date = pd.DataFrame(columns=['days_btw_diagnosis_surgery','days_btw_diagnosis_death','days_btw_diagnosis_first_treatment', 'days_btw_first_last_schema'])

# We create a new categorical variable that says whether the patient has died, and concat it to df_cat
df_yes_no = pd.DataFrame(columns=['death'])
df_cat = pd.concat([df_cat, df_yes_no], ignore_index=True)

# "Automatically" select the columns
dx_date=df.filter(regex='diagnosis|dx').columns
first_treat=df.filter(regex='first_treat').columns
rec_year=df.filter(regex='recurrence|rec').columns
death_year=df.filter(regex='death_year|death_date').columns

# We transform the dates to d-m-y format and do the substraction between 2 dates
def reformate_date (i, j, date_2, title, df_):
    if df.iloc[j][i] != 'Missing values' and df.iloc[j][date_2] != 'Missing values':
        first_date = str(df.iloc[j][i])
        second_date = str(df.iloc[j][date_2])
        formatted_date1 = datetime.strptime(first_date, "%d/%m/%Y")
        formatted_date2 = datetime.strptime(second_date, "%d/%m/%Y")
        df_.loc[j, title] = (formatted_date2 - formatted_date1).total_seconds() / 86400

# We substract the surgery date, the death date, and the first treatment date, to the diagnosis date
for i in df.columns:
    if i == dx_date[0]:
        for j in range(df.shape[0]):
            reformate_date(i, j, 'surgery_date_1', 'days_btw_diagnosis_surgery', df_date)
            reformate_date(i, j,death_year[0], 'days_btw_diagnosis_death', df_date)
            if df.iloc[j][i] != 'Missing values' and df.iloc[j]['death_date_1'] != 'Missing values':
                df_yes_no.loc[j, 'death'] = 'yes'
            if df.iloc[j][death_year[0]] == 'Missing values':
                df_yes_no.loc[j, 'death'] = 'no'
            reformate_date(i, j,first_treat[0], 'days_btw_diagnosis_first_treatment', df_date)


# Plot the dates

for i in df_date.columns:
    # Histogram
    plt.subplot(1, 2, 2)
    df_date[i].value_counts().hist()
    plt.title('Distribution')
    plt.ylabel("")
    plt.xlabel(i)
    plt.savefig("Date_variable_" + str(i), dpi=300)

    # Picts to ppt
    img_path = "Date_variable_" + str(i) + '.png'
    graph_slide_layout = ppt.slide_layouts[8]
    slide = ppt.slides.add_slide(graph_slide_layout)
    title = slide.shapes.title
    title.text = str(i)
    placeholder = slide.placeholders[1]
    pic = placeholder.insert_picture(img_path)
    subtitle = slide.placeholders[2]
    subtitle.text = ""

# Analysis of CATEGORICAL variables

for i in df_cat.columns:
    if df_cat[i].dtypes == 'O':
        df_cat[i] = df_cat[i].str.lower()

    if len(df_cat[i].value_counts()) <= 2:
        # Pie chart
        fig = plt.figure(figsize=(20, 5))
        df_cat.groupby(i).size().plot(kind='pie', textprops={'fontsize': 15},
                                      colors=['gold', 'blue'], autopct=lambda x: str(round(x, 2)) + '%',
                                      pctdistance=0.5)
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
        subtitle.text = str(len(df_cat[i].value_counts())) + " categories" + "\nSample size: " + str(len(df_cat)) +  " (" + str(round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100),2)) + " %)" + "\nMode: " + str(statistics.mode(df_cat[i]))

    else:
        # Bar chart
        fig = plt.figure()
        df_cat.groupby(i).size().plot(kind='bar', rot='vertical')
        plt.xticks(fontsize=5, rotation='vertical')
        plt.tight_layout()
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
            len(df_cat))  + " (" + str(
            round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100), 2)) + " %)" + "\nMode: " + str(statistics.mode(df_cat[i]))





# Analysis of QUANTITATIVE variables

# Delete variables with no values. Find the columns where each value is null
cols_empty = [col for col in df_num.columns if df_num[col].isnull().all()]
# Drop these columns from the dataframe
df_num.drop(cols_empty,
        axis=1,
        inplace=True)

for i in df_num.columns:
    print(i)
    # Box plot
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    df_num[i].dropna(axis=0).plot.box(fontsize=8)
    plt.title("Box plot")

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
    graph_slide_layout = ppt.slide_layouts[8]
    slide = ppt.slides.add_slide(graph_slide_layout)
    title = slide.shapes.title
    title.text = str(i)
    placeholder = slide.placeholders[1]
    pic = placeholder.insert_picture(img_path)
    subtitle = slide.placeholders[2]
    subtitle.text = "Variable " + str(i) + " has: " + str(len(outliers)) + " outliers" + "\nMean: " + str(round(np.nanmean(df_num[i]),2)) + "\nMedian: " + str(np.nanmedian(df_num[i])) + "\nMissing values: " + str(df_num[i].isnull().sum())






ppt.save("Datas_final.pptx")