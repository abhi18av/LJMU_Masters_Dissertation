#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np

# # Feature engineering for Resistance Profile

# In[69]:


tbprofiler_df = pd.read_json("../../data/raw/cohort.tbprofiler.json", encoding="UTF-8")
tbprofiler_df = tbprofiler_df.transpose()
# tbprofiler_df.head()


# In[86]:


# tbprofiler_df.shape


# In[70]:


resistance_status_df = tbprofiler_df
resistance_status_df['Resistance_Status'] = resistance_status_df.apply(
    lambda row: 'Sensitive' if (row.drtype == 'Sensitive') else 'Resistant', axis=1)
# resistance_status_df.head()


# In[94]:


resistance_status_df.to_csv("../../data/processed/resistance_status_df.tsv", "\t")
# resistance_status_df.head(10)


# In[72]:


drugs_column_names = ['rifampicin',
                      'isoniazid',
                      'pyrazinamide',
                      'ethambutol',
                      'streptomycin',
                      'fluoroquinolones',
                      'moxifloxacin',
                      'ofloxacin',
                      'levofloxacin',
                      'ciprofloxacin',
                      'aminoglycosides',
                      'amikacin',
                      'kanamycin',
                      'capreomycin',
                      'ethionamide',
                      'para-aminosalicylic_acid',
                      'cycloserine',
                      'linezolid',
                      'bedaquiline',
                      'clofazimine',
                      'delamanid']

lineage_column_names = ['main_lin', 'sublin']

resistance_status_column_names = ['drtype', 'MDR', 'XDR', 'Resistance_Status']

renamed_drug_columns_names = ['rifampicin_resistance',
                              'isoniazid_resistance',
                              'pyrazinamide_resistance',
                              'ethambutol_resistance',
                              'streptomycin_resistance',
                              'fluoroquinolones_resistance',
                              'moxifloxacin_resistance',
                              'ofloxacin_resistance',
                              'levofloxacin_resistance',
                              'ciprofloxacin_resistance',
                              'aminoglycosides_resistance',
                              'amikacin_resistance',
                              'kanamycin_resistance',
                              'capreomycin_resistance',
                              'ethionamide_resistance',
                              'para-aminosalicylic_acid_resistance',
                              'cycloserine_resistance',
                              'linezolid_resistance',
                              'bedaquiline_resistance',
                              'clofazimine_resistance',
                              'delamanid_resistance']

renamed_drug_columns_names_dict = {
    'rifampicin': 'rifampicin_resistance',
    'isoniazid': 'isoniazid_resistance',
    'pyrazinamide': 'pyrazinamide_resistance',
    'ethambutol': 'ethambutol_resistance',
    'streptomycin': 'streptomycin_resistance',
    'fluoroquinolones': 'fluoroquinolones_resistance',
    'moxifloxacin': 'moxifloxacin_resistance',
    'ofloxacin': 'ofloxacin_resistance',
    'levofloxacin': 'levofloxacin_resistance',
    'ciprofloxacin': 'ciprofloxacin_resistance',
    'aminoglycosides': 'aminoglycosides_resistance',
    'amikacin': 'amikacin_resistance',
    'kanamycin': 'kanamycin_resistance',
    'capreomycin': 'capreomycin_resistance',
    'ethionamide': 'ethionamide_resistance',
    'para-aminosalicylic_acid': 'para-aminosalicylic_acid_resistance',
    'cycloserine': 'cycloserine_resistance',
    'linezolid': 'linezolid_resistance',
    'bedaquiline': 'bedaquiline_resistance',
    'clofazimine': 'clofazimine_resistance',
    'delamanid': 'delamanid_resistance'
}

# In[74]:


resistance_status_df.rename(columns=renamed_drug_columns_names_dict,
                            inplace=True)

# resistance_status_df.head()


# In[79]:


binarized_resistance_status_df = resistance_status_df

for col_name in renamed_drug_columns_names:
    binarized_resistance_status_df[col_name] = resistance_status_df[col_name].apply(
        lambda resistance: 0 if resistance is '-' else 1)

# In[80]:


binarized_resistance_status_df.to_csv("../../data/processed/binarized_resistance_status_df.tsv", "\t")
