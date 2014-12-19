from Function_Module import *
import time, os, glob, csv, random
import multiprocessing as mp

from contextlib import contextmanager

@contextmanager
def cd(path):
    saved_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(saved_path)

def brief_pause(N):
    time.sleep((.1 + random.random()) / N)
    
def PB_func(cpath, kp, N):
    brief_pause(N)
    T1 = time.time()
    Instance_path = path(cpath,'Instance_{}'.format(kp))
    mkpath(Instance_path)
    
    ID = 'temp' + str(kp)
    
    cp('TPH.cs',       '{}/'.format(Instance_path))
    cp('WITP-TPH.exe', '{}/'.format(Instance_path))
    cp('WITPdataSet*', '{}/'.format(Instance_path))    
    
    with cd(Instance_path):
        command = "echo '' | mono WITP-TPH.exe"
        output = bash_command(command)
        temp_file = '../Solution_{}.txt'.format(ID)
        mv('*Sol*', temp_file)
    
    rm(Instance_path)   
    Last_line = output[-1]
    assert 'minimum cost' in Last_line

    S = float(Last_line.split()[-1])
    T = time.time() - T1
    
    brief_pause(N)
    
    k = len(glob.glob(cpath + '/Solution_*')) - mp.cpu_count()
    k = max([1, k])
        
    temp_file = '{}/Solution_{}.txt'.format(cpath, ID)
    sol_file = '{}/Solution_{}.txt'.format(cpath, k)
    while os.path.isfile(sol_file):
        k += 1
        sol_file = '{}/Solution_{}.txt'.format(cpath, k)
        
    mv(temp_file , sol_file)
    
    string =  'Instance {} of {}:\n'.format(k, N)
    string += '    RUN TIME [Bhanu]: ' + ptime(T) + '\n'
    string += '    MIN COST [Bhanu]: ' + curr(S) + '\n'
    print string

    with open('{}/Data.csv'.format(cpath), 'ab') as f:
        my_csv = csv.writer(f)
        my_csv.writerow((S, T))
        
    return S, T
     
     
def PBhanu(cpath, N):    
    BS, BT = [], []
    bi, bj = set(), set()
    
    rm(cpath + '/*')
    Instance_path = path(cpath,'Bhanu_Results')
    mkpath(Instance_path)
    rm(Instance_path + '/*')
    
    processes = []
    for k in xrange(1, N + 1):
        p = mp.Process(target=PB_func, args=(Instance_path, k, N))
        processes.append(p)
    
    M = mp.cpu_count()
    for proc in (processes[i:i+M] for i in range(0, N, M)):    
        for p in proc:
            p.start()

        for p in proc:
            p.join()
    
    for sol_file in glob.iglob(Instance_path + '/*Sol*'):    
        with open(sol_file, 'r') as f:
            lines = f.readlines()

        i, j = map(int, lines[-7].split()[1:3])
        bi.add(i)
        bj.add(j)
    
    cp('TPH.cs',       '{}/'.format(Instance_path))
    cp('WITP-TPH.exe', '{}/'.format(Instance_path))
    cp('WITPdataSet*', '{}/'.format(Instance_path))

    with open('{}/Bhanu_Results/Data.csv'.format(cpath), 'rb') as f:
        my_csv = csv.reader(f)
        BS, BT = [map(float, l) for l in zip(*my_csv)]

    _, BI = argmin(BS)
    
    f1 = '{}/Solution_{}.txt'.format(Instance_path, BI + 1)
    f2 = '{}/Best_Solution.txt'.format(Instance_path)
    cp(f1, f2)
    
    return sorted(tuple(bi)), sorted(tuple(bj))    



def Hybrid_code(cpath, N, GG=.02):
    T1 = time.time()
    bi, bj = PBhanu(cpath, N)
    BTT = time.time() - T1

    print bi
    print bj

    with open('{}/Bhanu_Results/Data.csv'.format(cpath), 'rb') as f:
        my_csv = csv.reader(f)
        BS, BT = [map(float, l) for l in zip(*my_csv)]
        
    print
    qprint('RESULTS [Bhanu]: ',t=0, n=0)
    qprint('TIME:  {0:.2f} seconds'.format(BTT),t=1, n=0)
    qprint('OBJ:  ' + curr(min(BS)),t=1, n=1)
    
    #for s in BS: print curr(s)
    
if __name__ == '__main__':
    Hybrid_code('Results/Test/Results_T12345', 6)
        
