#!/usr/bin/env nextflow

/*
#==============================================
code documentation
#==============================================
*/


/*
#==============================================
params
#==============================================
*/

params.saveMode = 'copy'
params.filePattern = "./*_{R1,R2}.fastq.gz"
params.resultsDir = 'results/trimmomatic'

Channel.fromFilePairs(params.filePattern)
        .into { ch_in_trimmomatic }


/*
#==============================================
trimmomatic
#==============================================
*/

process trimmomatic {

    publishDir params.resultsDir, mode: params.saveMode
    container 'quay.io/biocontainers/trimmomatic:0.35--6'

    input:
    tuple genomeName, file(genomeReads) from ch_in_trimmomatic

    output:
    tuple path(fq_1_paired), path(fq_2_paired) into ch_out_trimmomatic

    script:

    fq_1_paired = genomeName + '_R1.p.fastq'
    fq_1_unpaired = genomeName + '_R1.s.fastq'
    fq_2_paired = genomeName + '_R2.p.fastq'
    fq_2_unpaired = genomeName + '_R2.s.fastq'

    """
    trimmomatic \
    PE -phred33 \
    ${genomeReads[0]} \
    ${genomeReads[1]} \
    $fq_1_paired \
    $fq_1_unpaired \
    $fq_2_paired \
    $fq_2_unpaired \
    LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:36
    """
}


/*
#==============================================
# extra
#==============================================
*/
