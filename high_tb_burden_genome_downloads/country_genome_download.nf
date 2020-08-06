  /*
================================
params
================================
*/

params.resultsDir = 'results/rawGenomes'
// we can obtain this key from the NCBI portal
params.apiKey = "ed38c182ff2cdca964f0c766e220c02ec608"

/*
================================
ids of genomes to be downloaded
================================
*/


ids = [
]

  

/*
================================
only for publishing these files to results folder
================================
*/


process downloadRawGenomes {

    input:
    set genomeName, file(genomeReads) from Channel.fromSRA(ids, cache: true, apiKey: params.apiKey)

    errorStrategy 'ignore'

    script:
    
    """
    mkdir -p ../../../$params.resultsDir
    mv \$(readlink -f ${genomeReads[0]}) ../../../$params.resultsDir/
    mv \$(readlink -f ${genomeReads[1]}) ../../../$params.resultsDir/

    """


}
