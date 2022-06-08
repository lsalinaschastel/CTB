import pandas as pd
import numpy as np

# Introduce the name of the data file
file_name='chemotherapy'

# Read it
df = pd.read_csv(file_name + '.csv', sep=';')

# Group by patient
group=df.groupby(['ehr'])


dict_sust = {0: 'no', 1: 'yes'}

if len(df) == len(group.indices): # for Excels in which 1 row per patient, the only change we need to do is convert 0,1 to yes, no
    for col in df.columns:
        if set(df[col].value_counts().index) == {0, 1}:
            df[col] = df[col].replace(dict_sust)

    df.to_csv(file_name +'_transf2' +'.csv', sep=';')

else: # for Excels in which > 1 row per patient, we perform changes

    # Create new dataframe with ehr column
    ehrs = df['ehr'].unique()
    df_new = pd.DataFrame(ehrs)
    df_new.rename(columns={0: 'ehr'}, inplace=True)

    # Get max value of different values among all attributes
    df_grouped_max = df.groupby(['ehr']).count().reset_index()
    max_attribute = max(df_grouped_max.drop(['ehr'], axis=1).max())

    # Create in new df as many columns as max value of all attributes (except ehr)
    df_w_ehr = df.drop(['ehr'], axis=1)
    for col in df_w_ehr.columns:
        for i in range(1, max_attribute + 1):
            df_new[col + '_' + str(i)] = ""

        # Fill in columns
        row = 0
        for i in ehrs:
            new_col = []
            new_col = np.asarray(group.get_group(i)[col])
            for j in (range(1, len(new_col) + 1)):
                df_new.loc[row,col + '_' + str(j)] = new_col[j - 1]
            row += 1
    df_new.to_csv(file_name + '_transf2' + '.csv', sep=';')