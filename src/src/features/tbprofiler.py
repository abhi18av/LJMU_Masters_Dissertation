#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import the usual suspects.
import pandas as pd
import numpy as np



# # Feature engineering for Resistance Profile

# In[69]:


tbprofiler_df = pd.read_json("../data/raw/cohort.tbprofiler.json", encoding="UTF-8")
tbprofiler_df = tbprofiler_df.transpose()
#tbprofiler_df.head()


# In[86]:


#tbprofiler_df.shape


# In[70]:


resistance_status_df = tbprofiler_df
resistance_status_df['Resistance_Status'] = resistance_status_df.apply(lambda row: 'Sensitive' if (row.drtype == 'Sensitive') else 'Resistant', axis = 1)
#resistance_status_df.head()


# In[94]:


resistance_status_df.to_csv("../data/processed/resistance_status_df.csv")
#resistance_status_df.head(10)


# In[72]:


drugs_column_names = ['rifampicin',
