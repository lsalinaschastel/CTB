for i in df_date.columns:
    # Histogram
    plt.subplot(1, 2, 2)
    df_date[i].value_counts().hist()
    plt.ylabel("Frequency")
    plt.xlabel("Days")
    plt.savefig("Date_variable_" + str(i), dpi=300)

    # Picts to ppt
    img_path = "Date_variable_" + str(i) + '.png'
    graph_slide_layout = ppt.slide_layouts[8]
    slide = ppt.slides.add_slide(graph_slide_layout)
    title = slide.shapes.title
    title.text = str(i)
    placeholder = slide.placeholders[1]
    pic = placeholder.insert_picture(img_path)



# We create new variables that will be the result of operating with the dates
df_date = pd.DataFrame(columns=['Days between diagnosis and first surgery','Days between diagnosis and death','Days between diagnosis and first treatment', 'Days between first and last schema'])

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
            reformate_date(i, j, 'surgery_date_1', 'Days between diagnosis and first surgery', df_date)
            reformate_date(i, j,death_year[0], 'Days between diagnosis and death', df_date)
            if df.iloc[j][i] != 'Missing values' and df.iloc[j]['death_date_1'] != 'Missing values':
                df_yes_no.loc[j, 'death'] = 'yes'
            if df.iloc[j][death_year[0]] == 'Missing values':
                df_yes_no.loc[j, 'death'] = 'no'
            reformate_date(i, j,first_treat[0], 'Days between diagnosis and first treatment', df_date)

df_cat = pd.concat([df_cat, df_yes_no], ignore_index=True)

" (" + str(round(((df_cat[i].isnull().sum() / df_cat.shape[0]) * 100),2)) + " %)" +