#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np



vcf_snps_df = pd.read_csv("../../data/interim/cols_dropped_vcf_transposed_df.csv", "\t")

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

binary_unique_snps_df.to_csv("../data/interim/binary_unique_snps_df.csv")


