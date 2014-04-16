#!/usr/bin/python

import sys
import os

if __name__ == "__main__":

	if len(sys.argv) != 6:
		sys.exit("Usage: <infile> <outfile> <sym> <delta> <Nthreads>")
		
	volume_name = sys.argv[1]
	outfile = sys.argv[2]
	sym = sys.argv[3]
	delta = sys.argv[4]
	N = sys.argv[5]

	command = "e2project3d.py " + volume_name + " --outfile=" + outfile + " --orientgen=eman:delta=" + delta + ":inc_mirror=1 --sym=" + sym + " --projector=standard --parallel=thread:" + N + " -f"

	os.system(command)
