#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


vcf_snps_df = pd.read_csv("../../data/interim/cols_dropped_vcf_df.tsv", "\t")

vcf_snps_df = vcf_snps_df.rename(columns={'Unnamed: 0': 'SampleID'}).set_index('SampleID')


## FIXME we have completely ignored zygocity and have only focused on allel-pair-hetegenous
## https://gatk.broadinstitute.org/hc/en-us/articles/360035531912-Spanning-or-overlapping-deletions-allele-

def split_allele_pair(allele_pair):
    first_allele = list(allele_pair)[0]
    second_allele = list(allele_pair)[-1]
    return [first_allele, second_allele]

def compare_alleles(allele_pair):
    first_allele, second_allele = split_allele_pair(allele_pair)
    if first_allele == '.' or second_allele == '.':
        # NOTE return 0 for any variant which calls "."
        return 0
    else:
        return 1 if first_allele != second_allele else 0

def is_heterozygous_allele(allele_pair):
    # print(allele_pair)
    # print(compare_alleles(split_allele_pair(allele_pair)))
     compare_alleles(split_allele_pair(allele_pair))


# NOTE Finalize the rules for reducing the Allele patterns to Homozygous and Heterozygous
def is_heterozygous_vector(allele_vector):
     return list(map(lambda allele: compare_alleles(split_allele_pair(allele)), allele_vector))


binary_unique_snps_df= vcf_snps_df.apply(is_heterozygous_vector, axis=0)

binary_unique_snps_df.to_csv("../data/processed/binary_unique_snps_df.csv")


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
