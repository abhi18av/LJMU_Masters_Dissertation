    
  head -n 1 cohort.bqsr.filter.snps.indels.tsv >  cohort.bqsr.filter.snps.tsv 
  cat cohort.bqsr.filter.snps.indels.tsv | grep 'SNP' >>  cohort.bqsr.filter.snps.tsv 
