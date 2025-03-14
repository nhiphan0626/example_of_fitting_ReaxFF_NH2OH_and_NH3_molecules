import matplotlib.pyplot as plt
import pandas as pd
import os
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
			with open(i + '/' + 'nh2oh_configurations' + '/' + 'O-H-0.95985'+ '/' + 'qeq.eng') as f:
				data1 = f.readlines()
			for a, b in enumerate(data1): 
				if 'TotEng' in b:
					e_depth = float(data1[a+1].split()[1])
					#print(e_depth)
					
			with open( i +'/' + 'nh2oh_configurations' + '/'+ j +'/'+ 'qeq.eng') as f:
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



df = pd.read_csv('results.csv')

df['ffield_params'] = df['path'].apply(lambda x: x.split('/')[0])

mae_error = df.groupby('ffield_params')['error'].mean().reset_index()
with open('mae_error', 'w') as f:
	f.write(mae_error.to_string(index = False))

min_mae_error = mae_error.loc[mae_error['error'].idxmin()]
ffield_min = min_mae_error['ffield_params']
#print(ffield_min)
with open('min_error', 'w') as f:
	f.write(f"The minimum mae error from ffield(De, Re, L): {min_mae_error['ffield_params']}' with and the value error of {min_mae_error['error']} + '\n'")

get1 = df[df['ffield_params'] == min_mae_error['ffield_params']].reset_index()
data1 = get1.drop(get1.columns[[0, -1]], axis = 1)
#print(data1)
data1['distance'] = data1['path'].apply(lambda x: float(x.split('-')[-1]))
data1_NH3 = data1[data1['path'].str.contains('O-H')].sort_values(by = 'distance')
plt.figure(figsize=(6.5,5))

plt.plot(data1_NH3['distance'], data1_NH3['dft_dissociation_eng'], label='M06-2X(6-311++G**', color = 'blue', marker = 'o')
plt.plot(data1_NH3['distance'], data1_NH3['Reaxff_dissociation_eng'],label='ReaxFF-CuCHON-2017', color = 'red', marker = '^')


plt.xlim(0.5, 3.0)
plt.ylim(-40, 300)
plt.xlabel('Distance (angstrom)', fontsize = 14)
plt.ylabel('Energy (kcal/mol)', fontsize = 14)
plt.title('O-H bond', fontsize = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 14)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

plt.savefig('bond_distance_vs_energy.tif', dpi=100)


