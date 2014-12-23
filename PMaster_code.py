from Function_Module import *
import time, os, glob, csv, random
import multiprocessing as mp
from BigMModel import solve_big_m_model
from contextlib import contextmanager


BIG_M_TIMEOUT = 15 * 60 * 60


def brief_pause(N):
    time.sleep((3 * random.random()) / N)
    
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
    
    M = max([mp.cpu_count()-1, 2])
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
    
    #print ptime(BTT)
    #print bi
    #print bj

    with open('{}/Bhanu_Results/Data.csv'.format(cpath), 'rb') as f:
        my_csv = csv.reader(f)
        BS, BT = [map(float, l) for l in zip(*my_csv)]
        
    qprint('RESULTS [Bhanu]: ',t=0, n=0)
    qprint('TIME:  {0:.2f} seconds'.format(BTT),t=1, n=0)
    qprint('OBJ:  ' + curr(min(BS)),t=1, n=1)
    
    qprint('Optimality Gap: {:.2%}'.format(GG))
    
    qprint("Warm Big M Method:")

    Instance_path = path(cpath,'WBM_Method')
    mkpath(Instance_path)

    HS, HT = solve_big_m_model(PUTAWAY=list(bi), PICKING=list(bj),
                               time_limit=BIG_M_TIMEOUT - BTT,
                               gap=GG)

    cp('bigm_output.txt', '{}/'.format(Instance_path))
    cp('Pickled_Data', '{}/'.format(Instance_path))
    return min(BS), BTT, HS, time.time() - T1


@Timer
def BM_wrapper(cpath, GG=.02):
    qprint("Big M Benchmark:")

    Instance_path = path(cpath,'BigM_Benchmark')
    mkpath(Instance_path)

    PS, PT = solve_big_m_model(gap=GG, time_limit=BIG_M_TIMEOUT)

    cp('bigm_output.txt', '{}/'.format(Instance_path))
    cp('Pickled_Data', '{}/'.format(Instance_path))

    return PS


if '__main__' == __name__:
    ID = 'C' + id_generator(size=5)
    foldername = 'Results_' + ID
    overview = path(foldername,'Overview.txt')
    cpath = path(foldername,'Case_1')
    print ID
    (BS, BT, HS), HT = Hybrid_code(cpath, N=6)
    print ptime(HT)
    PS, PT = BM_wrapper(cpath)
    print ptime(PT)        
