from Function_Module import *
import time, os, glob, csv
import multiprocessing as mp
from BigMModel import solve_big_m_model
from contextlib import contextmanager


BIG_M_TIMEOUT = 12 * 60 * 60

@contextmanager
def cd(path):
    saved_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(saved_path)


def PB_func(cpath, k, N):
    T1 = time.time()
    Instance_path = path(cpath,'Instance_{}'.format(k))
    mkpath(Instance_path)
    
    ID = 'temp' + str(k)
    
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
    
    k = len(glob.glob(cpath + '/*Sol*'))
    temp_file = '{}/Solution_{}.txt'.format(cpath, ID)
    sol_file = '{}/Solution_{}.txt'.format(cpath, k)
    mv(temp_file , sol_file)
    
    print "Instance {} of {}:".format(k, N)
    qprint('RUN TIME [Bhanu]: ' + ptime(T), t=1)
    qprint('MIN COST [Bhanu]: ' + curr(S) , t=1, n=1)
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
        
    for p in processes:
        p.start()

    for p in processes:
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
    
    print ptime(BTT)
    print bi
    print bj

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
    
if __name__ == '__main__':
    Hybrid_code('Results/Test/Results_T12345', 6)
        
