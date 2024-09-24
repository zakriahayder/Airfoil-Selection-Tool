# Airfoil Selection Tool

The **Airfoil Selection Tool** is a Python-based tool that helps in analyzing various airfoils using XFOIL, generating aerodynamic data, and summarizing the results into a comprehensive PDF report. The tool processes multiple airfoils and calculates their polar data based on user-defined parameters such as Reynolds number, velocity, and angle of attack.

## Features

- **XFOIL Integration**: Automatically runs XFOIL simulations for various NACA airfoils.
- **Polar Data Extraction**: Extracts polar data for airfoils, including lift coefficient (CL), drag coefficient (CD), and lift-to-drag ratio.
- **Graphical Report**: Automatically generates plots for CL, CD, and CL/CD ratio over the angle of attack and compiles them into a PDF report.
- **Object-Oriented Structure**: The project is designed using an object-oriented approach, allowing for modular, maintainable, and reusable code.

## Object-Oriented Design

The program uses classes and functions to encapsulate the logic for various components:

- **Airfoil Data Processing**: The `analysis.py` file includes functions for processing the airfoil polar data files, extracting parameters such as the Reynolds number and plotting the relevant graphs.
- **Modular Design**: Each airfoil is handled independently, with methods for data extraction, plotting, and file management grouped logically.
- **Reusability**: The structure allows easy extension for handling new airfoil formats or additional aerodynamic data.

## Requirements

- Python 3.x
- Matplotlib
- Pandas
- XFOIL (Installed and accessible in the system)

## Installation

Clone the repository:

```bash
git clone https://github.com/zakriahayder/Airfoil-Selection-Tool.git
cd Airfoil-Selection-Tool
