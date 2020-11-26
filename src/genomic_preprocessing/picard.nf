#!/usr/bin/env nextflow

/*
#==============================================
code documentation
#==============================================
*/


/*
#==============================================
PARAMS
#==============================================
*/


/*
#----------------------------------------------
flags
#----------------------------------------------
*/

params.createSequenceDictionary = false
params.collectAlignmentSummaryMetrics = false
params.collectInsertSizeMetrics = false
/*
#----------------------------------------------
directories
#----------------------------------------------
*/

params.gatkMarkDuplicatesSparkResultsDir = 'results/gatk/markDuplicatesSpark'

params.createSequenceDictionaryResultsDir = 'results/picard/createSequenceDictionary'
params.collectAlignmentSummaryMetricsResultsDir = 'results/picard/collectAlignmentSummaryMetrics'
params.collectInsertSizeMetricsResultsDir =  'results/picard/collectInsertSizeMetrics'
/*
#----------------------------------------------
file patterns
#----------------------------------------------
*/

params.refFasta = "NC000962_3.fasta"
params.readsFilePattern = "./*_{R1,R2}.fastq.gz"

/*
#----------------------------------------------
misc
#----------------------------------------------
*/

params.saveMode = 'copy'

/*
#----------------------------------------------
channels
#----------------------------------------------
*/

Channel.value("$workflow.launchDir/$params.refFasta")
        .set { ch_refFasta }

Channel.fromPath("$params.gatkMarkDuplicatesSparkResultsDir/*bam")
        .into {
            ch_in_collectAlignmentSummaryMetrics;
            ch_in_collectInsertSizeMetrics
        }

/*
#==============================================
CreateSequenceDictionary
#==============================================
*/

process CreateSequenceDictionary {
    publishDir params.createSequenceDictionaryResultsDir, mode: params.saveMode
    container "quay.io/biocontainers/picard:2.23.4--0"

    when:
    params.createSequenceDictionary

    input:
    path refFasta from ch_refFasta

    output:
    file "*.dict" into ch_out_createSequenceDictionary


    script:
    refFastaName = refFasta.toString().split("\\.")[0]

    """
    picard CreateSequenceDictionary REFERENCE=${refFasta}  OUTPUT=${refFastaName}.dict
    """
}


/*
#==============================================
CollectAlignmentSummaryMetrics
#==============================================
*/

process CollectAlignmentSummaryMetrics {
    publishDir params.collectAlignmentSummaryMetricsResultsDir, mode: params.saveMode
    container "quay.io/biocontainers/picard:2.23.4--0"

    when:
    params.collectAlignmentSummaryMetrics

    input:
    path refFasta from ch_refFasta
    file(dedupedSortedBamFile) from ch_in_collectAlignmentSummaryMetrics

    output:
    file "*.txt" into ch_out_collectAlignmentSummaryMetrics


    script:
    refFastaName = refFasta.toString().split("\\.")[0]

    """
    picard CollectAlignmentSummaryMetrics R=${refFasta} I=${dedupedSortedBamFile}  O=${refFastaName}_alignment_metrics.txt
    """
}

/*
#==============================================
CollectInsertSizeMetrics
#==============================================
*/

process CollectInsertSizeMetrics {
    publishDir params.collectInsertSizeMetricsResultsDir, mode: params.saveMode
    container "quay.io/biocontainers/picard:2.23.4--0"

    when:
    params.collectInsertSizeMetrics

    input:
    file(dedupedSortedBamFile) from ch_in_collectInsertSizeMetrics

    output:
    tuple file("*.txt"),
            file("*pdf") into ch_out_collectInsertSizeMetrics


    script:

    """
    picard CollectInsertSizeMetrics INPUT=${dedupedSortedBamFile}  OUTPUT=${refFastaName}_insert_metrics.txt HISTOGRAM_FILE=${dedupedSortedBamFile}_insert_size_histogram.pdf
    """
}


/*
#==============================================
# extra
#==============================================
*/
