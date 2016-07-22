#!/bin/bash

##############################################
###  converts GenBank IDs to Taxonomy IDs  ###
##############################################

#input: file with list of genbank id numbers

FI=$1
FINAME=$(echo $FI | cut -d'.' -f 1)

if [ -f ${FINAME}_taxid.txt ]; then
   rm ${FINAME}_taxid.txt
fi

while read -r GI; do
   curl -s "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${GI}&rettype=gb" |\
   grep 'db_xref="taxon:' |\
   cut -d ':' -f 2 |\
   cut -d '"' -f 1  >> ${FINAME}_taxid_eutils.txt
done < $FI
