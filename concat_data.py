
import pandas as pd

df_patient = pd.read_csv('patient_transf.csv', sep=';', index_col=0)
df_chemotherapy = pd.read_csv('chemotherapy_transf.csv', sep=';', index_col=0)
df_radiotherapy = pd.read_csv('radiotherapy_transf.csv', sep=';', index_col=0)
df_surgery = pd.read_csv('surgeries_transf.csv', sep=';', index_col=0)
df_family = pd.read_csv('family_transf.csv', sep=';', index_col=0)
df_comorbidity = pd.read_csv('list_comorbidity_handmade.csv', sep=';')

df_final1=pd.merge(df_patient,df_chemotherapy, on='ehr',how='outer')
df_final2=pd.merge(df_final1,df_radiotherapy, on='ehr',how='outer')
df_final3=pd.merge(df_final2,df_surgery, on='ehr',how='outer')
df_final4=pd.merge(df_final3,df_family, on='ehr',how='outer')
df_final=pd.merge(df_final4,df_comorbidity, on='ehr',how='outer')

df_final.to_csv('concat_data_final.csv', sep=';')

