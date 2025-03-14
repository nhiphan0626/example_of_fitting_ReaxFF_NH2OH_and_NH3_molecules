import numpy as np
import os
import shutil

#Place the source directory in the same directory
source_dirs=['nh2oh_configurations']

#Place the script to generate ffield.RexPoN in the same directory
generate_force_field='generate_ffield.py'

for d in [0.0283]:
    for r in [1.2885]:
        for l in [10.9190]:
            
            dir_name = f"{d:.4f}_{r:.4f}_{l:.4f}"
            
            os.system('mkdir ' + dir_name)
            
            #Run the external script to generate ffield.RexPoN
            os.system(f'python {generate_force_field} {d} {r} {l}')
                
            shutil.copy('ffield.Reaxff', dir_name)
            
            #Copy source directories (O_head and H_down) to each created directory
            for src_dir in source_dirs:
                dest_dir=os.path.join(dir_name, src_dir)
                
                
                shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
                
                #Copy ffield.RexPoN to every subdirectory 
                for root, dirs, _ in os.walk(dest_dir):
                    for sub_dir in dirs:
                        target_dir= os.path.join(root,sub_dir)
                        shutil.copy('ffield.Reaxff',target_dir)
        
print("All directories and files have been processed successfully!")
            
