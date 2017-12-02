from multiprocessing import Pool
from tidservice import TIDService
import sql
import json
import calendar
import time

thing = TIDService(conn=sql.Sql("resources/stress.db"))

def f(x):
    return thing.grab_tids(x,"698d4d2ed8c1")

with open('resources/stressfiles.json', 'r') as fil:
    files = json.load(fil)
fil.close()


if __name__ == '__main__':
    files=list(map(lambda x : "/dom/base/"+x,files))
    start = calendar.timegm(time.gmtime())
    p = Pool(5)
    print(len(list(p.map(f, files)))) #remove p to test sequentially
    end = calendar.timegm(time.gmtime())
    print(end-start)
    print("end")
