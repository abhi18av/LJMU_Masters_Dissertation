#!/usr/bin/env python
# coding: utf-8

import pandas as pd

vcf_snps_df = pd.read_csv("../../data/interim/head100_cols_dropped_vcf_transposed_df.tsv", "\t")

vcf_snps_df = vcf_snps_df.rename(columns={'Unnamed: 0': 'SampleID'}).set_index('SampleID')

col_mutation_dict = {}

for col in vcf_snps_df.columns:
    col_unique_values = list(vcf_snps_df[col].unique())
    if len(col_unique_values) > 1:
        col_mutation_dict[col] = dict(vcf_snps_df[col].value_counts())
        print(col)

with open("../../data/interim/head100_cols_with_mutations_dict.txt", "w") as outfile:
    outfile.write(str(col_mutation_dict))

vcf_unique_snps_df = vcf_snps_df[list(col_mutation_dict.keys())]
vcf_unique_snps_df.to_csv("../../data/interim/head100_vcf_unique_snps_df.tsv", "\t")
