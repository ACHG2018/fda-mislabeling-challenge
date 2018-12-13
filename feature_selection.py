#!/usr/bin/env/python3
import pandas as pd
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as pyp
import sys
import os


train_rna=pd.read_csv('train_rna_common.tsv', sep='\t')
train_pro=pd.read_csv('train_pro_common.tsv',sep='\t')

train_rna['median'] = train_rna.median(axis=1)
train_pro['median'] = train_pro.median(axis=1)

train_rna_md=train_rna.sub(train_rna.median(axis=1),axis=0)
train_pro_md=train_pro.sub(train_pro.median(axis=1),axis=0)	

train_rna_md=train_rna_md.abs()
train_pro_md=train_pro_md.abs()

feature_corr=(round(train_rna_md.corrwith(train_pro_md,axis=1),2))

#with pd.option_context('display.max_rows',None,'display.max_columns', None): print (feature_corr.abs() )

feature_corr.to_csv("feature_corr.tsv", sep="\t")


fig, ax = pyp.subplots()
feature_corr.hist(ax=ax)
fig.savefig('fig.png')

os.system("awk '{if ($2 >= 0.5) print $0}' feature_corr.tsv > corrs_gte5.tsv")
os.system("awk '{print $1}' corrs_gte5.tsv | xargs -I {} sed '{}q;d' train_pro_common_labels.tsv | cut -f1 > corrs_gte5_genes.txt")
os.system("cat corrs_gte5_genes.txt | xargs -I {} grep -w -m1 {} train_pro.tsv > train_pro_selected_features.tsv")
os.system("cat corrs_gte5_genes.txt | xargs -I {} grep -w -m1 {} train_rna.tsv > train_rna_select_features.tsv")
