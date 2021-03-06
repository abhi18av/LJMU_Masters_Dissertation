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
vcf_df.to_csv("../../data/interim/cold_dropped_vcf_df.csv", "\t")
#vcf_df.head()
#
## In[18]:
#
#
#
# vcf_snps_df = pd.read_csv("../data/processed/vcf_df.csv")
#
#
## In[13]:
#
#
#vcf_snps_df = vcf_snps_df.rename(columns={'Unnamed: 0': 'SampleID'}).set_index('SampleID')
#vcf_snps_df.head()
#
#
## In[19]:
#
#
#col_mutation_dict = {}
#
#for col in vcf_snps_df.columns:
#    col_unique_values = list(vcf_snps_df[col].unique())
#    if len(col_unique_values) > 1:
#        # print('col: ', col, "\tsum: ", col_sum)
#        col_mutation_dict[col] =  dict(vcf_snps_df[col].value_counts())
#
#
## In[15]:
#
#
#col_mutation_dict
#
#
## In[20]:
#
#
#list(col_mutation_dict.keys())
#
#
## In[21]:
#
#
#import orjson
#
#col_mutation_dict_json = orjson.dumps(col_mutation_dict,
#                     # outfile,
#                     option=orjson.OPT_SERIALIZE_NUMPY )
#
#
#with open("../data/processed/cols_with_mutations.json", "wb") as outfile:
#    outfile.write(col_mutation_dict_json)
#
#
## In[ ]:
#
#
#with open("../data/processed/cols_with_mutations.txt", "w") as outfile:
#    outfile.write(str(col_mutation_dict))
#
#
## In[22]:
#
#
#dict(vcf_snps_df['NC000962_3.11'].value_counts())
#
#
## In[23]:
#
#
#vcf_unique_snps_df =  vcf_snps_df[list(col_mutation_dict.keys())]
#vcf_unique_snps_df.to_csv("../data/processed/vcf_unique_snps_df.csv")
#vcf_unique_snps_df.head()
#
#
## In[33]:
#
#
## FIXME we have completely ignored zygocity and have only focused on allel-pair-hetegenous
## https://gatk.broadinstitute.org/hc/en-us/articles/360035531912-Spanning-or-overlapping-deletions-allele-
#
#def split_allele_pair(allele_pair):
#    first_allele = list(allele_pair)[0]
#    second_allele = list(allele_pair)[-1]
#    return [first_allele, second_allele]
#
#def compare_alleles(allele_pair):
#    first_allele, second_allele = split_allele_pair(allele_pair)
#    if first_allele == '.' or second_allele == '.':
#        # NOTE return 0 for any variant which calls "."
#        return 0
#    else:
#        return 1 if first_allele != second_allele else 0
#
#def is_heterozygous_allele(allele_pair):
#    # print(allele_pair)
#    # print(compare_alleles(split_allele_pair(allele_pair)))
#     compare_alleles(split_allele_pair(allele_pair))
#
#
## NOTE Finalize the rules for reducing the Allele patterns to Homozygous and Heterozygous
#def is_heterozygous_vector(allele_vector):
#     return list(map(lambda allele: compare_alleles(split_allele_pair(allele)), allele_vector))
#
#
## list(map(lambda allele_pair: is_heterozygous(allele_pair),
##          vcf_df['ERR3129939'].unique()))
#
#
## In[34]:
#
#
#
#binary_unique_snps_df= vcf_unique_snps_df.apply(is_heterozygous_vector, axis=0)
#binary_unique_snps_df.head()
#
#
## In[35]:
#
#
#binary_unique_snps_df.to_csv("../data/processed/binary_unique_snps_df.csv")
#
#
## In[36]:
#
#
#
## binary_unique_snps_df = pd.read_csv("../data/processed/binary_unique_snps_df.csv")
#binary_unique_snps_df.head()
#
#
## In[9]:
#
#
#binary_unique_snps_df = binary_unique_snps_df.rename({'Unnamed: 0': 'SampleID'}).set_index('SampleID')
#binary_unique_snps_df.head()
#
#
## In[32]:
#
#
#binary_unique_snps_df['NC000962_3.78'].sum()
#
#
## In[40]:
#
#
#binary_unique_snps_df.head()
#
#
## In[38]:
#
#
## Ensure that every column has atleast one mutation
#
#binary_col_mutation_dict = {}
#
#for col in binary_unique_snps_df.columns:
#    sum_of_col = binary_unique_snps_df[col].sum()
#    if  sum_of_col > 0:
#        # print('col: ', col, "\tsum: ", col_sum)
#        binary_col_mutation_dict[col] =  dict(binary_unique_snps_df[col].value_counts())
#
#binary_col_mutation_dict
#
#
## In[41]:
#
#
#
#len(list(binary_col_mutation_dict.keys()))
#
#
## In[45]:
#
#
#hetero_binary_vcf_snps_with_mutations_df= binary_unique_snps_df[list(binary_col_mutation_dict.keys())]
#
## hetero_binary_vcf_snps_with_mutations_df.to_csv("../data/processed/hetero_binary_vcf_snps_with_mutations_df.csv")
#
#
## In[5]:
#
#
#hetero_binary_vcf_snps_with_mutations_df = pd.read_csv("../data/processed/hetero_binary_vcf_snps_with_mutations_df.csv")
#
## hetero_binary_vcf_snps_with_mutations_df = pd.read_csv("../data/processed/hetero_binary_vcf_snps_with_mutations_df.csv", index_col='SampleID')
#
## hetero_binary_vcf_snps_with_mutations_df = binary_unique_snps_df[list(binary_col_mutation_dict.keys())]
#
#hetero_binary_vcf_snps_with_mutations_df.head()
#
#
## In[14]:
#
#
#hetero_binary_vcf_snps_with_mutations_df.head()
#
#
## In[16]:
#
#
#hetero_binary_vcf_snps_with_mutations_df = hetero_binary_vcf_snps_with_mutations_df.rename(columns= {'Unnamed: 0': 'SampleID'}).set_index('SampleID')
#
#hetero_binary_vcf_snps_with_mutations_df.head()
#
#
## In[ ]:
#
#
#hetero_binary_vcf_snps_with_mutations_df.shape
#
#
## In[ ]:
#
#
#hetero_binary_vcf_snps_with_mutations_df.isnull().values.any()
#
#
## # Creation of the final dataframe
#
## In[ ]:
#
#
#hetero_binary_vcf_snps_with_mutations_df.head()
#
#
## In[ ]:
#
#
#final_df = binarized_resistance_status_df.join(hetero_binary_vcf_snps_with_mutations_df)
#
#final_df.head(10)
#
#
## In[ ]:
#
#
#final_df.shape
#
#
## In[ ]:
#
#
#final_df.to_csv("../data/processed/binarized_final_df.csv")
#
#
## In[ ]:
#
#
#final_df.head()
#
#
## In[ ]:
#
#
#final_df['Resistance_Status']
#
#
## In[ ]:
#
#
#
#
#
## In[6]:
#
#
#
#
#
## In[7]:
#
#
#hetero_binary_vcf_snps_with_mutations_df.isnull().values.any()
#
#
## # Creation of the final dataframe
#
## In[49]:
#
#
#hetero_binary_vcf_snps_with_mutations_df.head()
#
#
## In[17]:
#
#
#final_df = binarized_resistance_status_df.join(hetero_binary_vcf_snps_with_mutations_df)
#
#final_df.head(10)
#
#
## In[18]:
#
#
#final_df.shape
#
#
## In[19]:
#
#
#final_df.to_csv("../data/processed/binarized_final_df.csv")
#
#
## In[21]:
#
#
#final_df.head()
#
#
## In[93]:
#
#
#final_df['Resistance_Status']
#
#
## In[ ]:
#
#
#
#
