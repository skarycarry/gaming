import tkinter as tk
import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Ensure that FactorApp and ComparisonApp are imported from the correct module
from game_scripts import FactorApp, ComparisonApp, TextSaverApp

def read_names_from_file(file_path):
    with open(file_path, 'r') as file:
        names = file.read().splitlines()
    return names

def get_existing_columns(csv_path):
    if Path(csv_path).exists():
        df = pd.read_csv(csv_path)
        return df.columns.tolist()
    return []

def main():
    csv_path = Path(__file__).parent.parent / 'data' / 'comparisons.csv'  # Path to the CSV file
    names_file_path = Path(__file__).parent.parent / 'games.txt'  # Path to the text file with names
    names = read_names_from_file(names_file_path)
    existing_columns = get_existing_columns(csv_path)

    # Include names ending with '*' and names not in existing columns
    names_to_process = [name for name in names if name not in existing_columns or name.endswith('*')]

    for name in names_to_process:
        # Strip '*' from the name for processing
        clean_name = name.rstrip('*')
        
        factor_app = FactorApp(clean_name)
        comparison_app = ComparisonApp(clean_name)
        
        factor_app.root.mainloop()
        comparison_app.root.mainloop()
        text_app = TextSaverApp(clean_name)

if __name__ == "__main__":
    main()
