#!/usr/bin/env Rscript
finame = commandArgs(trailingOnly=TRUE)
finm <- strsplit(finame,'\\.')[[1]][1]
if (length(finame) != 1){
	stop('the name a file containing \\n-separated GenBank identifiers must be provided as input')
}
library(reutils)
gi.fi <- as.list(read.table(finame))
post.list <- epost(gi.fi[[1]],'protein')
ncbi.results <- efetch(post.list, db='protein', rettype='fasta', outfile = paste(finm,'.ncbi.out',sep=''))

taxids <- list()
outfi <- paste(finm,'.taxids.txt',sep='')
conversion.fi <- readLines(paste(finm,'.ncbi.out',sep=''))
gi.boo <- FALSE
tax.boo <- FALSE
for (entry in conversion.fi){
  if (! gi.boo && length(strsplit(entry,'<TSeq_gi>')[[1]]) > 1){
    gi <- strsplit(strsplit(entry,'<TSeq_gi>')[[1]][2],'</TSeq_gi>')[[1]][1]
    gi.boo <- TRUE
  }else if (gi.boo && ! tax.boo && length(strsplit(entry,'<TSeq_taxid>')[[1]]) > 1){
    taxid <- strsplit(strsplit(entry,'<TSeq_taxid>')[[1]][2],'</TSeq_taxid>')[[1]][1]
    tax.boo <- TRUE
  }else if (gi.boo && tax.boo){
    write(paste(gi,taxid,sep='\t'),outfi,append=TRUE)
    gi.boo <- FALSE
    tax.boo <- FALSE
  }
}