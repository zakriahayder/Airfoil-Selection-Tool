# analysis.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class AirfoilPolarData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.airfoil_name = self.extract_airfoil_name()
        self.reynolds_number = self.extract_reynolds_number()
        self.data = self.read_data()
        self.calculate_max_cl_cd()
    
    def extract_airfoil_name(self):
        with open(self.file_path, "r") as file:
            for line in file:
                if "Calculated polar for:" in line:
                    return line.split(":")[-1].strip()
        return "Unknown Airfoil"
    
    def extract_reynolds_number(self):
        with open(self.file_path, "r") as file:
            for line in file:
                if "Re =" in line:
                    parts = line.split("Re =")[1].split()
                    re_number = parts[0] + "E" + parts[2]  # Combine number and exponent
                    return float(re_number)
        return None  # Return None if not found
    
    def read_data(self):
        column_names = ["alpha", "CL", "CD", "CDp", "CM", "Top_Xtr", "Bot_Xtr"]
        data = pd.read_csv(self.file_path, sep="\s+", skiprows=12, names=column_names)
        return data
    
    def calculate_max_cl_cd(self):
        self.data['CL/CD'] = self.data['CL'] / self.data['CD']
        self.max_cl_cd_index = self.data['CL/CD'].idxmax()
        self.max_cl_cd_alpha = self.data.at[self.max_cl_cd_index, 'alpha']
        self.max_cl_cd = self.data.at[self.max_cl_cd_index, 'CL/CD']
        self.max_cl = self.data.at[self.max_cl_cd_index, 'CL']
        self.max_cd = self.data.at[self.max_cl_cd_index, 'CD']

class AirfoilPlotter:
    def __init__(self, airfoil_data):
        self.airfoil_data = airfoil_data

    def create_plots(self, pdf, page_number):
        airfoil_name = self.airfoil_data.airfoil_name
        reynolds_number = self.airfoil_data.reynolds_number
        data = self.airfoil_data.data
        max_cl_cd_alpha = self.airfoil_data.max_cl_cd_alpha
        max_cl_cd = self.airfoil_data.max_cl_cd
        max_cl = self.airfoil_data.max_cl
        max_cd = self.airfoil_data.max_cd

        # Create plots
        fig, axes = plt.subplots(3, 1, figsize=(8, 11))
        plt.suptitle(
            f"{airfoil_name}, Re = {reynolds_number:.3e}",
            fontsize=16,
            fontweight="bold",
        )

        # Plot CL vs alpha
        axes[0].plot(data["alpha"], data["CL"], label="CL", color="blue")
        axes[0].axvline(max_cl_cd_alpha, color="grey", linestyle="--")
        axes[0].axhline(max_cl, color="grey", linestyle="--")
        axes[0].text(
            max_cl_cd_alpha,
            max_cl,
            f"({max_cl_cd_alpha:.2f}, {max_cl:.4f})",
            verticalalignment="bottom",
            horizontalalignment="right",
        )
        axes[0].set_xlabel("Angle of Attack (α)")
        axes[0].set_ylabel("Lift Coefficient (CL)")
        axes[0].set_title(f"CL vs. α ({airfoil_name})")
        axes[0].grid(True)

        # Plot CD vs alpha
        axes[1].plot(data["alpha"], data["CD"], label="CD", color="green")
        axes[1].axvline(max_cl_cd_alpha, color="grey", linestyle="--")
        axes[1].axhline(max_cd, color="grey", linestyle="--")
        axes[1].text(
            max_cl_cd_alpha,
            max_cd,
            f"({max_cl_cd_alpha:.2f}, {max_cd:.4f})",
            verticalalignment="bottom",
            horizontalalignment="right",
        )
        axes[1].set_xlabel("Angle of Attack (α)")
        axes[1].set_ylabel("Drag Coefficient (CD)")
        axes[1].set_title(f"CD vs. α ({airfoil_name})")
        axes[1].grid(True)

        # Plot CL/CD vs alpha
        axes[2].plot(data["alpha"], data["CL/CD"], label="CL/CD", color="red")
        axes[2].axvline(max_cl_cd_alpha, color="grey", linestyle="--")
        axes[2].axhline(max_cl_cd, color="grey", linestyle="--")
        axes[2].text(
            max_cl_cd_alpha,
            max_cl_cd,
            f"({max_cl_cd_alpha:.2f}, {max_cl_cd:.4f})",
            verticalalignment="bottom",
            horizontalalignment="right",
        )
        axes[2].set_xlabel("Angle of Attack (α)")
        axes[2].set_ylabel("Lift-to-Drag Ratio (CL/CD)")
        axes[2].set_title(f"CL/CD vs. α ({airfoil_name})")
        axes[2].grid(True)

        # Add annotations at the bottom of the page
        plt.figtext(
            0.5,
            0.02,
            f"At α = {max_cl_cd_alpha:.2f}: CL = {max_cl:.4f}, CD = {max_cd:.4f}, Max CL/CD = {max_cl_cd:.4f}",
            ha="center",
            fontsize=10,
            bbox={"facecolor": "orange", "alpha": 0.5, "pad": 5},
        )

        # Add page number at the bottom right of the page
        plt.figtext(0.95, 0.02, f"Page {page_number}", ha="right", fontsize=10)

        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        pdf.savefig(fig)  # Save the current figure to PDF
        plt.close()

class AirfoilReport:
    def __init__(self, directory_path, pdf_path):
        self.directory_path = directory_path
        self.pdf_path = pdf_path
        self.airfoil_data_list = self.load_airfoil_data()
    
    def load_airfoil_data(self):
        airfoil_data_list = []
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.directory_path, filename)
                airfoil_data = AirfoilPolarData(file_path)
                airfoil_data_list.append(airfoil_data)
        return airfoil_data_list
    
    def sort_airfoils(self):
        # Sort airfoils by increasing max CL value
        self.airfoil_data_list.sort(key=lambda x: x.max_cl)
    
    def generate_pdf_report(self):
        with PdfPages(self.pdf_path) as pdf:
            page_number = 1
            self.create_title_page(pdf, page_number)
            page_number += 1
            self.create_table_of_contents(pdf, page_number)
            page_number += 1

            for airfoil_data in self.airfoil_data_list:
                plotter = AirfoilPlotter(airfoil_data)
                plotter.create_plots(pdf, page_number)
                page_number += 1
    
    def create_title_page(self, pdf, page_number):
        title_page = plt.figure(figsize=(8, 11))
        title_page.clf()
        title_page.text(
            0.5,
            0.5,
            "Airfoil Analysis Report",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
        )
        plt.figtext(0.95, 0.02, f"Page {page_number}", ha="right", fontsize=10)
        pdf.savefig(title_page)
        plt.close()
    
    def create_table_of_contents(self, pdf, page_number):
        toc_page = plt.figure(figsize=(8, 11))
        toc_page.clf()
        toc_page.text(
            0.5,
            0.9,
            "Table of Contents",
            ha="center",
            va="center",
            fontsize=16,
            fontweight="bold",
        )
        for i, airfoil_data in enumerate(self.airfoil_data_list, start=1):
            toc_page.text(
                0.1,
                0.8 - 0.05 * i,
                f"{i}. {airfoil_data.airfoil_name}, CL at Max CL/CD: {airfoil_data.max_cl:.4f}",
                ha="left",
                va="top",
                fontsize=12,
            )
            toc_page.text(
                0.9,
                0.8 - 0.05 * i,
                f"Page {i + 2}",
                ha="right",
                va="top",
                fontsize=12,
            )
        plt.figtext(0.95, 0.02, f"Page {page_number}", ha="right", fontsize=10)
        pdf.savefig(toc_page)
        plt.close()

if __name__ == "__main__":
    # Replace with the path to your directory and desired PDF output path
    directory_path = "polar data"
    pdf_path = "airfoil_analysis_report.pdf"
    report = AirfoilReport(directory_path, pdf_path)
    report.sort_airfoils()
    report.generate_pdf_report()
    print("PDF report generated successfully.")
