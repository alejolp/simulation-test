#!/usr/bin/env python
# coding: utf-8

import simpy, random, math

Count = None
M = None
Q = None
Buff = None 

def producer(env, t):
    while True:
        yield Q.put(1)
        yield env.timeout(t)

def worker(env, t):
    global M, Q, Buff, Count
    while True:
        yield Q.get(1)
        Count += 1

        yield Buff.put(1)
        yield env.timeout(t)
        yield Buff.get(1)

def sampler(env, t):
    global M, Q, Buff
    while True:
        M.append(Buff.level)
        yield env.timeout(t)

def avg(T):
    return 1.0 * sum(T) / len(T)

def var(T):
    a = avg(T)
    return math.sqrt(sum([(x - a)**2 for x in T]) / len(T))

def run(T):
    global M, Q, Buff, Count

    print "WORKERS N={}, Tavg={}, Tvar={}".format(len(T), avg(T), var(T))

    env = simpy.Environment()

    Count = 0
    M = []
    Q = simpy.Container(env)
    Buff = simpy.Container(env)

    env.process(producer(env, 0.5))

    for i in range(len(T)):
        env.process(worker(env, T[i % len(T)]))

    env.process(sampler(env, 1))
    env.run(until=150000)

    print "OCCUPANCY AVG={} MAX={} VAR={} COUNT={}".format(1.0 * sum(M) / len(M), max(M), var(M), Count)
    print 

def main():
    mu = 100

    N = 100
    #T1 = [95.30155957132754, 77.8260951443959, 78.49257525081191, 71.18808482838399, 52.74326358793528, 73.36612510766632, 74.92783050050127, 94.81187058839754, 78.28141093267628, 67.34813407980309, 92.43411238971146, 103.5287471661668, 56.53241031737829, 91.31986518000399, 75.46543556023643, 83.77976855967373, 76.67420439581328, 59.90987243182407, 60.71190539805219, 58.087147609513025]
    #T1 = [random.gauss(mu, 10) for x in range(N)] + [random.uniform(0, 2 * mu) for x in range(N)]
    #T1 = [random.uniform(0, 2 * mu) for x in range(N)]
    #T1 = [random.expovariate(1.0 / mu) for x in range(N)]

    print "GAUSS DISTRIBUTION:"

    T1 = [random.gauss(mu, 20) for x in range(N)]
    T2 = [1.0 * sum(T1) / len(T1)] * len(T1)

    run(T1)
    run(T2)

    print "UNIFORM DISTRIBUTION:"

    T1 = [random.uniform(0, 2 * mu) for x in range(N)]
    T2 = [1.0 * sum(T1) / len(T1)] * len(T1)

    run(T1)
    run(T2)

    print "EXP DISTRIBUTION:"

    T1 = [random.expovariate(1.0 / mu) for x in range(N)]
    T2 = [1.0 * sum(T1) / len(T1)] * len(T1)

    run(T1)
    run(T2)

    print "GAMMA DISTRIBUTION:"

    T1 = [random.gammavariate(4.0, mu / 4.0) for x in range(N)]
    T2 = [1.0 * sum(T1) / len(T1)] * len(T1)

    run(T1)
    run(T2)

if __name__ == '__main__':
    main()
