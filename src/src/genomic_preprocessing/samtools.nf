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


params.index = false
params.faidx = false
params.sort = false
params.depth = false

params.gatkMarkDuplicatesSparkResultsDir = 'results/gatk/markDuplicatesSpark'
params.bwaMemResultsDir = 'results/bwa/mem'

params.faidxResultsDir = 'results/samtools/faidx'
params.sortResultsDir = 'results/samtools/sort'
params.indexResultsDir = 'results/samtools/index'
params.depthResultsDir = 'results/samtools/depth'

params.saveMode = 'copy'

params.refFasta = "NC000962_3.fasta"
params.readsFilePattern = "./*_{R1,R2}.fastq.gz"
params.bamFilePattern = ".bam"
params.sortedBamFilePattern = ".sort.bam"


Channel.value("$workflow.launchDir/$params.refFasta")
        .set { ch_refFasta }

Channel.fromFilePairs(params.readsFilePattern)
        .set { ch_in_samtools }

Channel.fromPath("${params.bwaMemResultsDir}/*${params.bamFilePattern}")
        .set { ch_in_sort }

Channel.fromPath("${params.gatkMarkDuplicatesSparkResultsDir}/*${params.sortedBamFilePattern}")
        .into { ch_in_index; ch_in_depth }


/*
#==============================================
faidx
#==============================================
*/

process faidx {
    publishDir params.faidxResultsDir, mode: params.saveMode
    container 'quay.io/biocontainers/samtools:1.10--h2e538c0_3'

    when:
    params.faidx

    input:
    path refFasta from ch_refFasta

    output:
    file('*.fai') into ch_out_faidx

    script:

    """
    samtools faidx $params.refFasta
    """
}


/*
#==============================================
sort
#==============================================
*/

process sort {
    publishDir params.sortResultsDir, mode: params.saveMode
    container 'quay.io/biocontainers/samtools:1.10--h2e538c0_3'

    when:
    params.sort

    input:
    file(bamRead) from ch_in_sort

    output:
    file("*${params.sortedBamFilePattern}") into ch_out_sort

    script:

    genomeName = bamRead.toString().split("\\.")[0]
    """
    samtools sort ${bamRead} >  ${genomeName}.sort.bam
    """
}


/*
#==============================================
index
#==============================================
*/


process index {
    publishDir params.indexResultsDir, mode: params.saveMode
    container 'quay.io/biocontainers/samtools:1.10--h2e538c0_3'

    when:
    params.index

    input:
    path refFasta from ch_refFasta
    file(sortedBam) from ch_in_index

    output:
    file("*.bai") into ch_out_index

    script:

    """
    samtools index ${sortedBam}
    """
}


/*
#==============================================
depth
#==============================================
*/


process depth {
    publishDir params.depthResultsDir, mode: params.saveMode
    container 'quay.io/biocontainers/samtools:1.10--h2e538c0_3'

    when:
    params.depth

    input:
    path refFasta from ch_refFasta
    file(sortedBam) from ch_in_depth

    output:
    file("*.txt") into ch_out_depth

    script:
    genomeName = sortedBam.toString().split("\\.")[0]

    """
    samtools depth ${sortedBam} > ${genomeName}_depth_out.txt
    """
}


/*
#==============================================
# extra
#==============================================
*/

