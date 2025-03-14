import os, sys, glob

files = glob.glob('nh2oh_configurations' + '/' + 'H-O-N-*')

for file in files:
	print(file)
	os.system('cp lammps.in %s'%file)
