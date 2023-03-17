#!/usr/bin/env python3

import json
import os
import subprocess

def run_notebook(notebook_file, output_file, **arguments):
    """Pass arguments to a Jupyter notebook, run it and convert to html."""
    # Create the arguments file
    with open(".nbconfig", "w") as file:
        json.dump(arguments, file)
    # Run the notebook
    subprocess.call(
        [
            "jupyter-nbconvert",
            "--execute",
            "--no-input",
            "--to", "html",
            "--output", output_file,
            notebook_file,
        ]
    )
    os.remove(".nbconfig")

PATH = "/home/lars/Documents/mt/dtn7-lab/shared/scenarios/"

for scenario in os.scandir(PATH):
    for iter in os.scandir(scenario.path):
        if iter.is_dir() and "results" in iter.path:
            print(iter.path)
            run_notebook("analysis.ipynb", f"{iter.path}/report.html", path=f"{iter.path}/")
