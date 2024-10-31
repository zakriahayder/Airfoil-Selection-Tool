# Airfoil Selection Tool

The **Airfoil Selection Tool** is a Python-based tool that helps in analyzing various airfoils using XFOIL, generating aerodynamic data, and summarizing the results into a comprehensive PDF report. The tool processes multiple airfoils and calculates their polar data based on user-defined parameters such as Reynolds number, velocity, and angle of attack.

## Features

- **XFOIL Integration**: Automatically runs XFOIL simulations for various NACA airfoils.
- **Polar Data Extraction**: Extracts polar data for airfoils, including lift coefficient (CL), drag coefficient (CD), and lift-to-drag ratio.
- **Graphical Report**: Automatically generates plots for CL, CD, and CL/CD ratio over the angle of attack and compiles them into a PDF report.
- **Single and Batch Processing**: Analyze a single airfoil or multiple airfoils in one run.
- **Object-Oriented Structure**: The project is designed using an object-oriented approach, allowing for modular, maintainable, and reusable code.

## Object-Oriented Design

The program uses classes and functions to encapsulate the logic for various components:

- **Airfoil Data Processing**: The `analysis.py` file includes functions for processing the airfoil polar data files, extracting parameters such as the Reynolds number and plotting the relevant graphs.
- **Modular Design**: Each airfoil is handled independently, with methods for data extraction, plotting, and file management grouped logically.
- **Reusability**: The structure allows easy extension for handling new airfoil formats or additional aerodynamic data.

## Usage

### Running the Tool

1. **Single Airfoil Analysis**: Use `main.py` to run an XFOIL analysis for a single specified airfoil (e.g., "NACA0012") with predefined parameters. This script generates a polar data file for the specified airfoil.

   ```bash
   python main.py
   ```

2. **Multiple Airfoil Analysis**: Use `test.py` to analyze multiple NACA 4-digit airfoils. This script prompts the user for the number of airfoils, their digits, chord length, and freestream velocity, then generates polar data files for each airfoil and compiles a PDF report.

   ```bash
   python test.py
   ```

### Output

- The tool generates polar data files for each analyzed airfoil and compiles a PDF report (`airfoil_analysis_report.pdf`) containing the analysis results and plots.

## Requirements

- Python 3.x
- Matplotlib
- Pandas
- Numpy
- XFOIL (Installed and accessible in the system)

## Installation

Clone the repository:

```bash
git clone https://github.com/zakriahayder/Airfoil-Selection-Tool.git
cd Airfoil-Selection-Tool
```

Install the required Python packages:

```bash
pip install pandas matplotlib numpy
```

Ensure that XFOIL is installed and accessible in your system's PATH.

## Conclusion

The Airfoil Selection Tool provides a comprehensive solution for analyzing airfoils, making it easier for engineers and researchers to obtain and visualize aerodynamic data efficiently.