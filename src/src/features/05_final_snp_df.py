#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# TODO use transposed df
binary_unique_snps_df = pd.read_csv("../data/interimm/binary_unique_snps_df.tsv", "\t")

binary_unique_snps_df = binary_unique_snps_df.rename({'Unnamed: 0': 'SampleID'}).set_index('SampleID')

## Ensure that every column has atleast one mutation

binary_col_mutation_dict = {}

for col in binary_unique_snps_df.columns:
    sum_of_col = binary_unique_snps_df[col].sum()
    if sum_of_col > 0:
        # print('col: ', col, "\tsum: ", col_sum)
        binary_col_mutation_dict[col] = dict(binary_unique_snps_df[col].value_counts())
        print(col)

hetero_binary_vcf_snps_with_mutations_df = binary_unique_snps_df[list(binary_col_mutation_dict.keys())]

hetero_binary_vcf_snps_with_mutations_df.to_csv("../data/processed/hetero_binary_vcf_snps_with_mutations_df.tsv", "\t")

## hetero_binary_vcf_snps_with_mutations_df = pd.read_csv("../data/processed/hetero_binary_vcf_snps_with_mutations_df.csv", index_col='SampleID')

hetero_binary_vcf_snps_with_mutations_df = binary_unique_snps_df[list(binary_col_mutation_dict.keys())]

# hetero_binary_vcf_snps_with_mutations_df = hetero_binary_vcf_snps_with_mutations_df.rename(columns= {'Unnamed: 0': 'SampleID'}).set_index('SampleID')

binarized_resistance_status_df = pd.read_csv("../data/processed/binarized_resistance_status_df.tsv", "\t").rename(
    columns={'Unnamed: 0': 'SampleID'}).set_index('SampleID')

## Creation of the final dataframe

final_df = binarized_resistance_status_df.join(hetero_binary_vcf_snps_with_mutations_df)

final_df.to_csv("../data/processed/binarized_final_df.tsv", "\t")
