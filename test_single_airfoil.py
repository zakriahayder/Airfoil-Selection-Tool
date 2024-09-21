"""
Runs an XFOIL analysis for a given NACA 4-digit airfoil and flow conditions
"""
import os
import subprocess
import numpy as np

# %% User Inputs

# Prompt for the last four digits of the NACA 4-digit airfoil
digits = input("Enter the last 4 digits of the NACA 4-digit airfoil (e.g., 2412): ")

# Prompt for chord length (in meters)
c = float(input("Enter the chord length of the airfoil in meters (e.g., 1.0): "))

# Prompt for freestream velocity (in m/s)
V = float(input("Enter the freestream velocity in m/s (e.g., 10.0): "))

# Kinematic viscosity of air at standard conditions (m^2/s)
nu = 1.4607e-5

# Calculate Reynolds number
Re = (V * c) / nu
print("Calculated Reynolds number: {:.0f}".format(Re))

# Angle of attack range and step
alpha_i = 0
alpha_f = 10
alpha_step = 0.25

# Number of iterations
n_iter = 100

# %% XFOIL Input File Writer

# Remove existing polar file if it exists
if os.path.exists("polar_file.txt"):
    os.remove("polar_file.txt")

# Write the XFOIL input commands to 'input_file.in'
with open("input_file.in", 'w') as input_file:
    input_file.write("NACA {0}\n".format(digits))
    input_file.write("PANE\n")
    input_file.write("OPER\n")
    input_file.write("Visc {0}\n".format(int(Re)))
    input_file.write("PACC\n")
    input_file.write("polar_file.txt\n\n")
    input_file.write("ITER {0}\n".format(n_iter))
    input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f, alpha_step))
    input_file.write("\n\n")
    input_file.write("quit\n")

# %% Run XFOIL

# Execute XFOIL with the input file
subprocess.call("xfoil.exe < input_file.in", shell=True)

# %% Read and Process Polar Data

# Load the polar data from the generated polar file
polar_data = np.loadtxt("polar_file.txt", skiprows=12)

# Display the loaded polar data (optional)
print("Polar data loaded successfully.")
