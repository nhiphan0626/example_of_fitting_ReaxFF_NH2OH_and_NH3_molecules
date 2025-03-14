import os, sys, glob

files = glob.glob('nh2oh_configurations' + '/' + 'H-N-O-*')

for file in files:
	print(file)
	os.system('cp lammps.in %s'%file)
