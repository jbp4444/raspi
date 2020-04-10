#!/usr/bin/python

import random
import multiprocessing as mp

maxiter = 10000000

def worker( arg1 ):
	count = 0

	for i in range(maxiter):
		x = random.uniform(-1,1)
		y = random.uniform(-1,1)

		d2 = x*x + y*y

		if( d2 < 1 ):
			count = count + 1

	print( count, maxiter, 4*float(count)/float(maxiter) )

pool = mp.Pool(processes=4)
pool.map( worker, range(4) )

