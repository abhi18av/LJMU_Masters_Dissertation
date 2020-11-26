/*
================================
params
================================
*/

params.resultsDir = 'results/rawGenomes'
// we can obtain this key from the NCBI portal
params.apiKey = "PERSONAL_KEY"

/*
================================
ids of genomes to be downloaded
================================
*/


ids = [
'SRR1765871',
'SRR1765872',
]

  

/*
================================
only for publishing these files to results folder
================================
*/


process downloadRawGenomes {

    input:
    set genomeName, file(genomeReads) from Channel.fromSRA(ids, cache: true, apiKey: params.apiKey)

    script:
    
    """
    mkdir -p ../../../$params.resultsDir
    mv \$(readlink -f ${genomeReads[0]}) ../../../$params.resultsDir/
    mv \$(readlink -f ${genomeReads[1]}) ../../../$params.resultsDir/

    """


}
