import os
import pandas as pd
import numpy as np
import fnmatch 

df = pd.read_csv('./data_dft.csv')
dft = np.transpose(df.to_numpy())


list_dir = os.listdir('./')

list_ff = []
e_diss = []
result = []
for i in list_dir:
	if fnmatch.fnmatch(i,'??????_??????_*.*'):
		list_config = dft[0]
		list_ff.append(str(i))
		for j in list_config:
			with open(i + '/' + 'NH3-config' + '/' + 'NH3-1.0201'+ '/' + 'qeq.eng') as f:
				data1 = f.readlines()
			for a, b in enumerate(data1): 
				if 'TotEng' in b:
					e_depth = float(data1[a+1].split()[1])
					#print(e_depth)
					
			with open( i +'/' + 'NH3-config' + '/'+ j +'/'+ 'qeq.eng') as f:
				data2 = f.readlines()
			for m, n in enumerate(data2):
				if 'TotEng' in n:
					e_diss_RexPoN = (float(data2[m+1].split()[1]) - e_depth)
					#print(e_diss)
					index = np.where(dft[0] == j)[0]
					if len(index) > 0:
						e_diss_dft = dft[1][index[0]]
						error = (float(abs(e_diss_RexPoN - e_diss_dft)))
						result.append([i + '/' + j, e_diss_dft, e_diss_RexPoN, error ])
result_df = pd.DataFrame(result, columns = ['path', 'dft_dissociation_eng', 'Reaxff_dissociation_eng', 'error'])
result_df.to_csv('results.csv', index = False)
print('Done')
#print(result)
