import numpy as np
import sys
import os
cwd = os.getcwd()

from MCKLD import Rel_ent,Exp_rel_ent

RE=Rel_ent(cwd + '/REdata/chain.out',cwd + '/REdata/lnprior.out',False)
re=RE.Run()
print(re)
functions_path=cwd+'/Functions.py'
ERE=Exp_rel_ent(cwd+'/EREdata/D1_sample.txt',cwd+'/EREdata/C.txt',cwd+'/Functions.py',10)
ere=ERE.Run(300)
print('ere is:')
print(ere)
#pere=ERE.PRun(2,300)
