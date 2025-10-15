#!/bin/bash
# Assignment 5, Question 1: Project Setup Script
# This script creates the directory structure for the clinical trial analysis project
# TODO: Make this script executable (if not already)
# chmod +x q1_setup_project.sh

# TODO: Create the following directories:
#   - data/
#   - output/
#   - reports/

echo "Creat data, output, reports directories"
mkdir -p data output reports
echo "Directories created."

# TODO: Generate the dataset
#       Run: python3 generate_data.py
#       This creates data/clinical_trial_raw.csv with 10,000 patients

echo "Generate dataset"
python3 generate_data.py
echo "Dataset generated at data/clinical_trial_raw.csv"

# TODO: Save the directory structure to reports/directory_structure.txt
#       Hint: Use 'ls -la' or 'tree' command

echo "Save directory structure to reports/directory_structure.txt"
tree > reports/directory_structure.txt
echo "Directory strusource datasci-practice/bin/activatecture saved to reports/directory_structure.txt"

chmod +x q1_setup_project.sh
