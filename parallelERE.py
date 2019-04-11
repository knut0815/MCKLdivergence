import sys
import numpy as np
from numpy.linalg import inv
import os
cwd = os.getcwd()
from mpi4py import MPI
import time


nn=int(sys.argv[1])
ll=int(sys.argv[2])
s_path = str(sys.argv[3])
sample=np.genfromtxt(s_path)
l_path = str(sys.argv[4])
like_cov=np.genfromtxt(l_path)
fun_path = str(sys.argv[5])
mfunction=np.genfromtxt(fun_path)
ere=0
ti=0

from mfunction.Functions import model_function
mf=model_function()

#This function has been used in the code
def MAH_Distance(x,y):
     return np.transpose(x)@y@x

def jfun(i,l,data,sample,cov_like_inv):
     ss=0
     fl=float(l)
     for j in range(l):
          ss=ss+np.exp(-0.5*MAH_Distance(data[i]-mf.fun(sample[j]),cov_like_inv))
     term2 = np.log(ss/fl)
     term1 = -0.5*MAH_Distance(data[i]-mf.fun(sample[i]),cov_like_inv)
     return term1-term2

def expecte_relative_entropy(sample,likelihood_cov,n,l):
     #genertaing data sample
     fl=float(l)
     cov_like_inv = inv(likelihood_cov)
     data = np.zeros((l,n))
     for i in range(l):
          data[i] = np.random.multivariate_normal(mf.fun(sample[i]), likelihood_cov) 
     comm = MPI.COMM_WORLD
     rank = comm.Get_rank()
     size = comm.Get_size()

     a = 1
     perrank = l//size
     summ = np.zeros(1)

     comm.Barrier()
     start_time = time.time()
     temp = 0
     for k in range(a + rank*perrank, a + (rank+1)*perrank):
         temp = temp + jfun(k-1,l,data,sample,cov_like_inv)

     summ[0] = temp

     if rank == 0:
         total = np.zeros(1)
     else:
         total = None

     comm.Barrier()
     #collect the partial results and add to the total sum
     comm.Reduce(summ, total, op=MPI.SUM, root=0)

     stop_time = time.time()

     if rank == 0:
         print ("The res: ", total[0]/fl)
         print ("time spent with ", size, " threads in milliseconds")
         print ("-----", int((time.time()-start_time)*1000), "-----")
         exp_res=total[0]/fl
         print(exp_res)
         ts=int((time.time()-start_time)*1000)
         return exp_res
ere=expecte_relative_entropy(sample,like_cov,nn,ll) 
if rank==0:
     print(ere)
     sys.exit(0)
