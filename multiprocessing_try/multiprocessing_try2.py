from multiprocessing import Pool
import statistics


def f(x):
    return statistics.mean(x)

if __name__=='__main__':
    x=[list(range(10)),list(range(20,30)),list(range(30,40)),list(range(40,50))]
    with Pool(5) as p:
        print(p.map(f,x))
