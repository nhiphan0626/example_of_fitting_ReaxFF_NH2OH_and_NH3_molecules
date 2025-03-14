import os
import numpy as np

# Input data from the uploaded file
atoms = [
    ('N', 0.67825668527533, -0.00001501033296, 0.15746202411265),
    ('H', 1.04494231110899, -0.81286523607629, -0.33100284081405),
    ('H', 1.04465343171697, 0.81361073146851, -0.32992900984308),
    ('H', -1.12233805894420, -0.00064589826133, 0.73476494007296),  # H3
    ('O', -0.71419436915709, -0.00008458679794, -0.13398511352849),
]

# Constants
h3_index = 3  # Index of H3
oxygen_index = 4  # Index of O

# Atomic masses and types
atomic_masses = {'H': 1.00794, 'N': 14.0067, 'O': 15.9990}
atomic_types = {'H': 1, 'N': 2, 'O': 3}

# Extract original H3 and O positions
h3_atom = np.array(atoms[h3_index][1:])
o_atom = np.array(atoms[oxygen_index][1:])

# Calculate the direction vector from O to H3 and normalize it
direction = h3_atom - o_atom
direction /= np.linalg.norm(direction)

# Generate new configurations and save to directories
base_directory = "nh2oh_configurations"
os.makedirs(base_directory, exist_ok=True)

for distance in [0.5, 0.6, 0.8, 0.95985, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0]:
    new_h3_position = o_atom + direction * distance
    new_atoms = atoms[:]
    new_atoms[h3_index] = ('H', *new_h3_position)

    # Create a directory for this configuration
    dir_name = os.path.join(base_directory, f"O-H-{distance:.1f}")
    os.makedirs(dir_name, exist_ok=True)

    # Write the configuration to a LAMMPS data file in the directory
    output_file = os.path.join(dir_name, "data_lammps")
    with open(output_file, 'w') as f:
        f.write("# LAMMPS data file written by OVITO Basic 3.11.1\n\n")
        f.write("5 atoms\n")
        f.write("3 atom types\n")
        f.write("0.0 25.0 xlo xhi\n")
        f.write("0.0 25.0 ylo yhi\n")
        f.write("0.0 25.0 zlo zhi\n\n")
        f.write("Masses\n\n")
        for element, mass in atomic_masses.items():
            f.write(f"{atomic_types[element]} {mass:.5f}  # {element}\n")
        f.write("\nAtoms  # atomic\n\n")
        for idx, atom in enumerate(new_atoms, start=1):
            atom_type = atomic_types[atom[0]]
            f.write(f"{idx} 1 {atom_type} 0 {atom[1]:.3f} {atom[2]:.3f} {atom[3]:.3f} 0 0 0\n")

print(f"Generated configurations stored in directory: {base_directory}")

