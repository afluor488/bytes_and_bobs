#script to convert REBASE HTML database file to fasta

import re 
import sys

html = sys.argv[1]
target_enz_dict = {}

with open(html,'r') as infi:
    webtext = infi.read()
    enzymes = re.findall("target=enz>(.*?)</",webtext)
    targets = re.findall("<font size=2><font size=2>(.*?)</",webtext)
    
print "number of entries =",len(enzymes),"enzymes,",len(targets),"targets"

for target,enzyme in zip(targets,enzymes):
    if target != '-':
        target = re.sub('\((.*?)\)','',target).strip()
        for t in target.split(', '):
            if t not in target_enz_dict:
                target_enz_dict[t] = []
            target_enz_dict[t].append(enzyme)

print len(target_enz_dict),"target sequences identified"

with open(html.split('.')[0]+'.fasta','w') as outfi:
    for target in target_enz_dict:
        outfi.write(">"+", ".join(target_enz_dict[target])+"\n"+target+"\n")
