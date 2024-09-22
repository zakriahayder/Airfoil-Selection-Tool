"""
Runs an XFOIL analysis for multiple NACA 4-digit airfoils and generates PDF reports
"""
import os
import subprocess
import numpy as np
from analysis import AirfoilReport  # Import the AirfoilReport class

# Ensure necessary modules are installed
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
    print("Installing required packages...")
    subprocess.check_call(["pip", "install", "pandas", "matplotlib"])

# %% User Inputs

# Prompt for the number of airfoils
num_airfoils = int(input("Enter the number of NACA 4-digit airfoils to analyze: "))

# List to store airfoil digits
airfoil_list = []

# Collect airfoil digits for each airfoil
for i in range(num_airfoils):
    digits = input(f"Enter the last 4 digits of NACA 4-digit airfoil #{i+1} (e.g., 2412): ")
    airfoil_list.append(digits)

# Prompt for chord length (in meters)
c = float(input("Enter the chord length of the airfoils in meters (e.g., 1.0): "))

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

# Create 'polar data' directory if it doesn't exist
if not os.path.exists("polar data"):
    os.makedirs("polar data")

# %% XFOIL Analysis for Each Airfoil

for digits in airfoil_list:
    airfoil_name = f"NACA {digits}"
    print(f"\nRunning XFOIL analysis for {airfoil_name}...")

    # Define filenames
    polar_filename = f"polar data/{digits}_polar.txt"
    input_filename = f"input_file.in"

    # Remove existing polar file if it exists
    if os.path.exists(polar_filename):
        os.remove(polar_filename)

    # Write the XFOIL input commands to 'input_file.in'
    with open(input_filename, 'w') as input_file:
        input_file.write(f"NACA {digits}\n")
        input_file.write("PANE\n")
        input_file.write("OPER\n")
        input_file.write(f"Visc {int(Re)}\n")
        input_file.write("PACC\n")
        input_file.write(f"{polar_filename}\n\n")
        input_file.write(f"ITER {n_iter}\n")
        input_file.write(f"ASeq {alpha_i} {alpha_f} {alpha_step}\n")
        input_file.write("\n\n")
        input_file.write("quit\n")

    # %% Run XFOIL

    # Execute XFOIL with the input file
    subprocess.call("xfoil.exe < input_file.in", shell=True)

    # %% Check for Polar Data

    if os.path.exists(polar_filename):
        print(f"Polar data for {airfoil_name} saved successfully.")
    else:
        print(f"Polar data for {airfoil_name} could not be generated.")

# %% Generate PDF Report

print("\nGenerating PDF report for all airfoils...")
pdf_report_path = "airfoil_analysis_report.pdf"
report = AirfoilReport("polar data", pdf_report_path)
report.sort_airfoils()
report.generate_pdf_report()
print("PDF report generated successfully.")
