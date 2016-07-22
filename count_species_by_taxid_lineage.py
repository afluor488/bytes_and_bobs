#!/usr/bin/env python 

import urllib2
import sys

#first argument = tax report in format downloaded for ncbi (http://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi) with full taxid lineage

tax_report = open(sys.argv[1],'r').read().split('\n')

ebi_prefix = 'http://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/tax-id/'
species_list = {'archaea':[],'bacteria':[],'other_eukaryotes':[],'viruses':[],'fungi':[]}
category_taxids = {-2:{'2':'bacteria','2759':'other_eukaryotes','2157':'archaea'},-1:{'10239':'viruses'},-4:{'4751':'fungi'}}

for entry in tax_report[1:]:
   taxid_list = entry.split('|')[-1].split()

   for taxid in taxid_list:
      url = urllib2.urlopen(ebi_prefix+taxid).read()
      rank = url.split('"rank": "')[1].split('"')[0]

      if rank == 'species':
         for level in sorted(category_taxids.keys()):
           for category in category_taxids[level]:
              try:
                 if taxid_list[level] == category: 
                    species_list[category_taxids[level][category]].append(taxid)
                    break
              except:
                 pass

for category in species_list:
   print category.upper() + ':'
   print 'number of taxids at species level = ' + str(len(species_list[category]))
   print 'number of species = ' + str(len(set(species_list[category])))
