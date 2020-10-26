#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

vcf_df = pd.read_csv("../../data/raw/head100_cohort.bqsr.filter.snps.tsv", sep='\t')

vcf_df['CHROM.POS'] = vcf_df.apply(lambda row: row.CHROM + "." + str(row.POS), axis=1)
vcf_df.drop(['CHROM', 'POS'], axis=1, inplace=True)

vcf_df.set_index('CHROM.POS', inplace=True)
vcf_df.columns = list(map(lambda column: column.split(".")[0], vcf_df.columns))
vcf_df.to_csv("../../data/interim/head100_cols_dropped_vcf_untransposed_df.tsv", "\t")

vcf_df = vcf_df.transpose()
vcf_df.to_csv("../../data/interim/head100_cols_dropped_vcf_transposed_df.tsv", "\t")
