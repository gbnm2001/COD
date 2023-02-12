import matplotlib.pyplot as plt
import os
import shutil
#shutil.rmtree('plots')
try:
    print('Creating plots dir')
    os.mkdir('plots')
except:
    print('plots dir already exists')
hflags = ['request queue size', 'waiting time','Maximum queue length','unblock messages','DRAM responses']
vflags = ['LLC misses', 'LLC requests']
vsum =0
num_cores = 16#int(input('Number of cores = '))
num_llc= 2#int(input('Number of llcs = '))
filepath = ''#input('file path = ')
filename = (filepath.split('/')[-1]).split('.')[0]
temp = [0]*num_llc

files = [1,2,3,4,5,7,8,9,12,13,14,15,16,17]
for id in hflags:
    for i in files:
        f = open(f'mixes-BSP2/mix{i}/simulation_cmd')
        idp = False
        vals = [[] for i in range(num_cores)]
        xs = []
        count=1
        for line in f:
            if(idp):
                try:
                    l = list(map(float, line.split()))
                except:
                    idp=False
                    vsum=0
                    continue
                for j in range(0,len(l)):
                    vals[j].append(l[j])
                xs.append(count)
                idp=False
                count+=1
                    
            if(id in line):
                idp=True
        fig, ax = plt.subplots(figsize=(20,10))
        for j in range(num_llc):
            plt.plot(xs,vals[j],label=f"cache {j}")
        plt.legend()
        plt.xlabel('Intervals seperated by 1M cycles')
        plt.ylabel(id)
        try:
            os.mkdir(f'plots/{id}')
        except:
            pass
        plt.savefig(f'plots/{id}/mix{i}',dpi=180,bbox_inches='tight')
        plt.clf()
        plt.close()
        
for id in vflags:
    for i in files:
        f = open(f'mixes-BSP2/mix{i}/simulation_cmd')
        vptr = 0
        vals = [[] for llc in range(num_llc)]
        xs = []
        temp = [0]*num_llc
        count=1
        for line in f:
            if(vptr>0):
                try:
                    l = list(map(float, line.split()[2:2+num_llc]))
                    for llc in range(num_llc):
                        temp[llc]+=l[llc]
                    vptr+=1
                except:
                    vptr=0
                    temp = [0]*num_llc
            if(vptr==num_cores+1):
                vptr=0
                for llc in range(num_llc):
                    vals[llc].append(temp[llc])
                    temp[llc] = 0
                xs.append(count)
                count+=1
            if(id in line):
                vptr=1
        fig, ax = plt.subplots(figsize=(20,10))

        for j in range(num_llc):
            plt.plot(xs,vals[j],label=f"cache {j}")
        plt.legend()
        plt.xlabel('Intervals seperated by 1M cycles')
        plt.ylabel(id)
        try:
            os.mkdir(f'plots/{id}')
        except:
            pass
        plt.savefig(f'plots/{id}/mix{i}',dpi=180,bbox_inches='tight')
        plt.clf()
        plt.close()
print('Output is in plots dir')
        
