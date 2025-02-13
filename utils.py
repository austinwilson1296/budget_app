import csv
import os
import sys

def add_row_to_csv(filename,row):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def open_with_default_app(filepath):
    """Opens the given file with its default application."""
    if sys.platform.startswith('darwin'):  # macOS
        os.system(f'open "{filepath}"')
    elif os.name == 'nt':  # Windows
        os.startfile(filepath)
    elif os.name == 'posix':  # Unix-like systems
        os.system(f'xdg-open "{filepath}"')
    else:
        print("Operating system not supported.")