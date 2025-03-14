import os, sys, glob

files = glob.glob('nh2oh_configurations' + '/' + 'O-H-*')

for file in files:
	print(file)
	os.system('cp lammps.in %s'%file)
