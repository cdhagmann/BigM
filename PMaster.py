from Function_Module import *
from PMaster_code import *
import sys


GAP = {'Test': 0,
       'S': .02,
       'P': .15,
       'M': .30,
       'L': .45}

def main(cpath, Type, N=6):
    overview = path(cpath,'Overview.txt')

    Pyomo_code = True
    GG = GAP.get(Type, .5)

    #print GG

    BS, BT, HS, HT = Hybrid_code(cpath, N=N, GG=GG)
    print

    PS, PT = BM_wrapper(cpath, GG=GG)

    print line('#',10)
    tee_print(overview,'RESULTS [Bhanu]: ',t=0, n=0)
    tee_print(overview,'TIME:  {0:.2f} seconds'.format(BT),t=1, n=0)
    tee_print(overview,'OBJ:  ' + curr(BS),t=1, n=1)

    tee_print(overview,'RESULTS [Hybrid]: ',t=0, n=0)
    tee_print(overview,'TIME:  {0:.2f} seconds'.format(HT),t=1, n=0)
    tee_print(overview,'OBJ:  ' + curr(HS),t=1, n=1)

    tee_print(overview,'RESULTS [Pyomo]: ',t=0, n=0)
    tee_print(overview,'TIME:  {0:.2f} seconds'.format(PT),t=1, n=0)
    tee_print(overview,'OBJ:  ' + curr(PS),t=1, n=2)

    tee_print(overview,'COMPARISON [Hybrid vs Bhanu]: ',t=0, n=0)
    comp_err = perr(BS - HS, HS)
    tee_print(overview,'ERROR: ' + comp_err,t=1, n=0)
    speedup = '{0:.2f}'.format( BT / HT )
    tee_print(overview,'SPEEDUP: ' + speedup,t=1, n=1)


    tee_print(overview,'COMPARISON [Hybrid vs Pyomo]: ',t=0, n=0)
    comp_err = perr(PS - HS, HS)
    tee_print(overview,'ERROR: ' + comp_err,t=1, n=0)
    speedup = '{0:.2f}'.format( PT / HT )
    tee_print(overview,'SPEEDUP: ' + speedup,t=1, n=2)



    print line('#',10) + '\n'

if '__main__' == __name__:
    try:
        Type = sys.argv[1]
    except IndexError:
        Type = 'Misc'

    ID = Type + id_generator(size=5)

    if Type in GAP:
        cpath = 'Results/{}/Results_{}'.format(Type, ID)
    else:
        cpath = 'Results/{}/Results_{}'.format('Misc', ID)
    overview = path(cpath,'Overview.txt')

    print ID
    main(cpath, Type)
    rm('*.pyc')
    rm('*.log')
    rm('*WITP*')
    rm('*cs')
    rm('Pickled_Data')
