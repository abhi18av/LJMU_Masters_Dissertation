#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import the usual suspects.
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns

#sns.set()


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


lineage_column_names = [ 'main_lin', 'sublin' ]

resistance_status_column_names = [ 'drtype', 'MDR', 'XDR', 'Resistance_Status' ]


renamed_drug_columns_names = [                     'rifampicin_resistance',
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


resistance_status_df.rename(columns = renamed_drug_columns_names_dict,
                            inplace=True)

#resistance_status_df.head()


# In[79]:


binarized_resistance_status_df = resistance_status_df

for col_name in renamed_drug_columns_names:
    binarized_resistance_status_df[col_name] = resistance_status_df[col_name].apply(lambda resistance: 0 if resistance is '-' else 1)

#binarized_resistance_status_df.head(10)


# In[80]:


binarized_resistance_status_df.to_csv("../data/processed/binarized_resistance_status_df.csv")


# In[3]:


#binarized_resistance_status_df = pd.read_csv("../data/processed/binarized_resistance_status_df.csv").rename(columns={'Unnamed: 0' : 'SampleID'}).set_index('SampleID')

#binarized_resistance_status_df.head(10)


#==============================================

#==============================================


## # Feature engineering for SNP
## 
## - TODO: Include INDELS if there's a need
#
## In[8]:
#
#
#vcf_df = pd.read_csv("../data/processed/mdrlatam_cohort.bqsr.filter.snps.indels.tsv", sep='\t')
#vcf_df.head()
#
#
## In[9]:
#
#
#vcf_df['CHROM.POS'] = vcf_df.apply(lambda row: row.CHROM + "." + str(row.POS) , axis = 1)
#vcf_df.head()
#
#
## In[10]:
#
#
#vcf_df.drop(['CHROM', 'POS'], axis=1, inplace= True)
#vcf_df.head()
#
#
## In[11]:
#
#
#vcf_df.set_index('CHROM.POS', inplace= True)
#vcf_df.columns = list(map (lambda column: column.split(".")[0], vcf_df.columns))
#vcf_df = vcf_df.drop(columns = ['HET', 'HOM-REF', 'HET-REF'], axis= 1)
#vcf_df[vcf_df.TYPE == 'SNP']
#vcf_df = vcf_df.transpose()
#vcf_df.to_csv("../data/processed/vcf_df.csv")
#vcf_df.head()
#
#
## In[12]:
#
#
#vcf_df = vcf_df.transpose()
#
#
## In[13]:
#
#
#vcf_df = vcf_df.drop(columns = ['HET', 'HOM-REF', 'HET-REF'], axis= 1)
#vcf_df.head()
#
#
## In[15]:
#
#
#vcf_df = vcf_df[vcf_df.TYPE == 'SNP']
#vcf_df.head()
#
#
## ## Continuing only with the SNPs
## 
## - TODO explore HET column
#
## In[18]:
#
#
#
## vcf_snps_df = pd.read_csv("../data/processed/vcf_df.csv")
#
#vcf_snps_df = vcf_df.drop(columns= ['TYPE'], axis= 1).transpose()
#
#vcf_snps_df.head()
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
