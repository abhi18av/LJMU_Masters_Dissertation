#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# # Feature engineering for SNP
# 
# - TODO: Include INDELS if there's a need

# In[8]:


vcf_df = pd.read_csv("../../data/raw/cohort.bqsr.filter.snps.tsv", sep='\t')
# with indels
#vcf_df = pd.read_csv("../../data/processed/cohort.bqsr.filter.snps.indels.tsv", sep='\t')
#vcf_df.head()


## In[9]:


vcf_df['CHROM.POS'] = vcf_df.apply(lambda row: row.CHROM + "." + str(row.POS) , axis = 1)
#vcf_df.head()
#
#
## In[10]:
#
#
vcf_df.drop(['CHROM', 'POS'], axis=1, inplace= True)
#vcf_df.head()
#
#
## In[11]:
#
#
vcf_df.set_index('CHROM.POS', inplace= True)
vcf_df.columns = list(map (lambda column: column.split(".")[0], vcf_df.columns))
vcf_df = vcf_df.drop(columns = ['HET', 'HOM-REF', 'HET-REF', 'TYPE'], axis= 1)
#vcf_df[vcf_df.TYPE == 'SNP']
vcf_df = vcf_df.transpose()
vcf_df.to_csv("../../data/interim/cols_dropped_vcf_df.csv", "\t")

