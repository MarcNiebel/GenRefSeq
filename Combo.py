"""
This program takes the cluster number, number of ambigious nucleotides, accession number and year (either collection date or publication(latter preferred)) from the .clstr file
generated from CDHIT and using the tip to root lengths calulated from traversing the tree generated from FastTree produces a tab delimited file
with this information

"""

import re
from ete3 import Tree
import argparse

#Construct to allow for user arugments to be passed to script below
parser=argparse.ArgumentParser()
parser.add_argument('-i','--input',help='clstr. file from CDHIT as input')
parser.add_argument('-i2', '--input2', help='Tree file from FastTree as input')
parser.add_argument('-o','--output', help='Writing to a tab delimited file with "Combo" at beginning')
args = parser.parse_args()

#Empty dictionaries which will be filled with relevant information from the two different files
clust_dict={}
year_dict={}
branlength_dict={}
no_N_dict={}
log_file=open("logfile.txt", "a")
tsv_file=open(args.output + ".tsv", "w")
tsv_file.write("Accession_no\t Year\t Tip-root dist\t Cluster_no\t NumberofNs\t \n")
#Opening the cluster file generated from CD-HIT
cdhit_file=open(args.input,"r")
#print "Relevant information is being pulled out of .clstr file from CD-HIT..."
#For each line looking for relevant information with a regular expresssion and then placing this information
#with the accession number into the relevant dictionary
cluster_cnt=0
for line in cdhit_file:
	clust_str=""
	acc_str=""
	no_n_str=""
	cluster=re.search(r'Cluster \d+', line)
	if cluster:
		cluster_cnt+=1
		cluster_str=str(cluster.group(0))
		cluster_str=re.sub('Cluster ', '', cluster_str)
	acc_no=re.search(r'\w{2}\d+.\d{1}_\d{4}|\w{2}_\d+.\d{1}_\d{4}',line)
	if acc_no:
		acc_str=str(acc_no.group())
		acc_str=re.sub('_\d{4}$','',acc_str)
		clust_dict[acc_str]=cluster_str
	year=re.search(r'_(19\d{2}|20\d{2})', line)
	if year:
		year_str=str(year.group())
		year_str=re.sub('_','',year_str)
		year_dict[acc_str]=year_str
	no_n=re.search(r'_N\d+', line)
	if no_n:
		no_n_str= no_n.group()	
		no_n_str=re.sub('_N','',no_n_str)
		no_N_dict[acc_str]=no_n_str
	
log_file.write("The number of clusters are:" + str(cluster_cnt))
log_file.close()
cdhit_file.close()

#print "Tree from FastTree program is being used to calculate root to leaf distances..."
#Passing in the tree generated by FastTree
FastTree=Tree(args.input2)
#Getting the root of the tree
root=FastTree.get_tree_root()
#Loop through each leaf of the tree
for leaf in FastTree:
	#Convert 'leaf' to string to allow manipulation
	leaf_str=str(leaf)
	acc_nu=re.search(r'\w{2}\d+.\d{1}_\d{4}|\w{2}_\d+.\d{1}_\d{4}',leaf_str)
	acc_nu=str(acc_nu.group())
	acc_nu=re.sub('_\d{4}$','',acc_nu)
	rt_lf=FastTree.get_distance(root,leaf)
	#Make a dictionary using acc_nu as key 
	branlength_dict[acc_nu]=rt_lf
	#Using the generated dictionaries to print the relevant information to a tab delimited file
	tsv_file.write(acc_nu + "\t" + year_dict[acc_nu] + "\t" + str(rt_lf) + "\t" + clust_dict[acc_nu] + "\t" + no_N_dict[acc_nu] + "\n")
tsv_file.close


