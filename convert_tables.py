import pandas as pd

file_name=''
df = pd.read_csv(file_name + '.csv', sep=';')

# Create new dataframe with as many rows as patients
ehrs = df['ehr'].unique()
df_new = pd.DataFrame(ehrs)

# Rename column to ehr, and create the new columns that we will need
df_new. rename(columns={0:'ehr'}, inplace=True)



for i in df.columns:
    if i != 'ehr':
        loc = 0
        k = 1
        for j in range(df.shape[0]):
            if j == 0:
                if set(df[i].value_counts().index) == {0,1}:
                    if df.loc[j, i] == 0:
                        df_new.loc[j, i + '_' + str(k)] = 'no'
                    if df.loc[j, i] == 1:
                        df_new.loc[j, i + '_' + str(k)] = 'yes'
                    #if df.loc[j, i] == 99:
                        #df_new.loc[j, i + '_' + str(k)] = ''
                else:
                    df_new.loc[loc, i + '_' + str(k)] = df.iloc[j][i]

            else:

                if df.loc[j]['ehr'] == df.iloc[j-1]['ehr']:
                    k += 1
                    print(k)
                    if set(df[i].value_counts().index) == {0,1}:
                        if df.loc[j, i] == 0:
                            df_new.loc[j, i + '_' + str(k)] = 'no'
                        if df.loc[j, i] == 1:
                            df_new.loc[j, i + '_' + str(k)] = 'yes'
                        #if df.loc[j, i] == 99:
                            #df_new.loc[j, i + '_' + str(k)] = ''
                    else:
                        df_new.loc[loc, i + '_' + str(k)] = df.iloc[j][i]


                else:
                    loc += 1
                    k = 1
                    if set(df[i].value_counts().index) == {0,1}:
                        if df.loc[j, i] == 0:
                            df_new.loc[j, i + '_' + str(k)] = 'no'
                        if df.loc[j, i] == 1:
                            df_new.loc[j, i + '_' + str(k)] = 'yes'
                        #if df.loc[j, i] == 99:
                            #df_new.loc[j, i + '_' + str(k)] = ''
                    else:
                        df_new.loc[loc, i + '_' + str(k)] = df.iloc[j][i]




df_new.to_csv(file_name + '_transf' + '.csv', sep=';')