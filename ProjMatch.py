#!/usr/bin/python

from EMAN2 import *
from sparx import *

import sys

if __name__ == "__main__":

	if len(sys.argv) != 6:
		sys.exit("Usage: <ave> <proj> <output_proj> <output_cc> <N>")
		
	ave = sys.argv[1]
	stack = sys.argv[2]
	outstack = sys.argv[3]
	output_txt = sys.argv[4]
	N_best = int(sys.argv[5])

	n = EMUtil.get_image_count(stack)
	im = get_image(ave)
	st_im = Util.infomask(im, None, True)
	im -= st_im[0]
	im /= st_im[1]

	size = im.get_xsize()/2

	p = EMData()

	cc_values = []
	w = 10
	o = []

	for i in range(0,n):	
		if i%1000 == 0:
			print round(100*float(i)/n,1), "%"
		
		p.read_image(stack, i)

		alpha, sx, sy, mir, peak = align2d(p, im)
		p = rot_shift2D(p, alpha, 0, 0, 0)
		o.append(alpha)

		#print alpha, peak

		st_p = Util.infomask(p, None, True)
		p -= st_p[0]
		p /= st_p[1]

		cc = ccfn(im, p)

		vec = []
		for ii in range(-w,w+1):
			for jj in range(-w,w+1):
				vec.append(cc.get(size-ii, size-jj))
		cc_values.append(max(vec))
		

	cc_values_sorted = sorted(cc_values)

	count = 0
	nmax = N_best
	outtxt = open(output_txt, 'w')
	for i in range(n-1,n-nmax-1,-1):
		index = cc_values.index(cc_values_sorted[i])
		p.read_image(stack, index)
		p = rot_shift2D(p, o[index], 0, 0, 0)
		p.write_image(outstack, count)
		line = str(index) + "\t" + str(cc_values_sorted[i]) + "\n"
		outtxt.write(line)
		count += 1

	outtxt.close()
