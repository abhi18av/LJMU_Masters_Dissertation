Application of ML for DRP using WGS data on MTB genomes.
==============================

This repository contains the code for my masters dissertation.


To execute the code, the following execution environments are recommended.

1. AWS/Azure Batch for genomic pre-processing.

2. Azure ML Studio for notebooks, with a decent server.


The rest of the instructions  are embedded within the `notebooks/FINAL/*ipynb` notebooks.


Project Organization
------------

    ├── LICENSE
    ├── README.md
    │
    ├── conda_enviroment.yml <- The minimal conda file needed to recreate the environment.
    ├── azure_enviroment.yml <- The conda file for the Azure ML studio.
    │
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             
    │      ├── ALL_FEATURES   <- Models trained on All features.
    │      │      ├── FINAL   
    │      │
    │      └── PCA300         <- Models trained on PCA300 features.
    │
    ├── notebooks          
    │   ├── FINAL          <- The final jupyter notebooks, named as per their execution order.
    │      └── 001_feature_engineering.ipynb
    │      └── 002_choose_limited_tbportals_genomes.ipynb <- Contains the SRA IDs of genomes, can be downloaded through download.nf
    │      └── 003_eda_mono_resistance.ipynb
    │      └── 004_model_grids.ipynb
    │      └── 005_stacked_ensemble.ipynb
    │      └── 006_pca_based_ml.ipynb
    │      └── 007_model_inspection_with_without_pca.ipynb
    │
    ├── src                
    │   ├── genomic_preprocessing           <- Scripts for genomic pre-processing
    │      └── nyu_gatk.sh
    │      └── download.nf
    │      └── bwa.nf
    │      └── fastqc.nf
    │      └── gatk.nf
    │      └── picard.nf
    │      └── samtools.nf
    │      └── tb_profiler.nf
    │      └── trimmomatic.nf
    │   
    │   
    │   ├── features       <- Scripts to turn raw VCF data into tabular data for modeling
    │       └── 01_tbprofiler.py
    │       └── 02_vcf_drop_cols.py
    │       └── 03_filter_unique_snps.py
    │       └── 04_binarize_vcf.py
    │       └── 05_final_snp_df.py

--------

