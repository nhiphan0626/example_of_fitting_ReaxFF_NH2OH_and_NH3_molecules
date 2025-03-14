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
h1_index = 1  # Index of H1
oxygen_index = 4  # Index of O
nitrogen_index = 0  # Index of N
start_angle = 70  # Starting H1-N-O angle (degrees)
end_angle = 170  # Ending H1-N-O angle (degrees)
angle_step = 10  # Angle increment (degrees)

# Atomic masses and types
atomic_masses = {'H': 1.00794, 'N': 14.00670, 'O': 15.99900}
atomic_types = {'H': 1, 'N': 2, 'O': 3}

# Extract original H1, O, and N positions
h1_atom = np.array(atoms[h1_index][1:])
o_atom = np.array(atoms[oxygen_index][1:])
n_atom = np.array(atoms[nitrogen_index][1:])

# Calculate the vector from N to H1 and the plane normal
n_to_h1 = h1_atom - n_atom
n_to_o = o_atom - n_atom
plane_normal = np.cross(n_to_o, n_to_h1)
plane_normal /= np.linalg.norm(plane_normal)

def rotate_vector_in_plane(vector, axis, angle):
    """
    Rotate a vector around a given axis by a specified angle (in radians).
    """
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    rotation_matrix = (
        cos_angle * np.eye(3) +
        sin_angle * np.array([[0, -axis[2], axis[1]],
                               [axis[2], 0, -axis[0]],
                               [-axis[1], axis[0], 0]]) +
        (1 - cos_angle) * np.outer(axis, axis)
    )
    return rotation_matrix @ vector

# Generate new configurations and save to directories
base_directory = "nh2oh_h1_configurations"
os.makedirs(base_directory, exist_ok=True)

for angle in [70.0, 80.0, 90.0, 100.0, 104.7460, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]:
    # Convert angle to radians and calculate the new position of H1
    angle_rad = np.radians(angle - 104.7460)  # Adjust for the initial angle
    new_n_to_h1 = rotate_vector_in_plane(n_to_h1, plane_normal, angle_rad)
    new_h1_position = n_atom + new_n_to_h1

    new_atoms = atoms[:]
    new_atoms[h1_index] = ('H', *new_h1_position)

    # Create a directory for this configuration
    dir_name = os.path.join(base_directory, f"H-N-O-{angle}")
    os.makedirs(dir_name, exist_ok=True)

    # Write the configuration to a LAMMPS data file
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

