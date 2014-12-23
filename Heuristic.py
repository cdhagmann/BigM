from Function_Module import *
from PMaster_code import *
import sys


if '__main__' == __name__:
    try:
        Type = sys.argv[1]
    except IndexError:
        Type = 'Misc'

    ID = Type + id_generator(size=5)

    if Type in ('Test', 'S', 'P', 'M', 'L'):
        cpath = 'Results/{}/Results_{}'.format(Type, ID)
    else:
        cpath = 'Results/{}/Results_{}'.format('Misc', ID)
    
    mkpath(cpath)
    overview = path(cpath,'Overview.txt')

    print ID
    try:
        PBhanu(cpath, 7)
    finally:
        rm('*.pyc')
        rm('*.log')
        rm('*WITP*')
        rm('*cs')
        rm('Pickled_Data')
        rm('*.txt')
