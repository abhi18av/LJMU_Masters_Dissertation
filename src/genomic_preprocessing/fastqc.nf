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
params.resultsDir = './results/fastqc'
params.filePattern = "./*.fastq.gz"

Channel.fromPath(params.filePattern)
        .set { ch_in_fastqc }


/*
#==============================================
fastqc
#==============================================
*/

process fastqc {
    publishDir params.resultsDir, mode: params.saveMode
    container 'quay.io/biocontainers/fastqc:0.11.9--0'

    input:
    path genomeRead from ch_in_fastqc

    output:
    tuple file('*.html'), file('*.zip') into ch_out_fastqc


    script:

    """
    fastqc *fastq*
    """
}

/*
#==============================================
# extra
#==============================================
*/
