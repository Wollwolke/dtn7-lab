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

# PATH = "../shared/scenarios/industrial/"
PATH = "../shared/scenarios/robocup/"

BOOK = "analysis.ipynb"
# BOOK = "analysis_industrial.ipynb"

for root, _, files in os.walk(PATH):
    if not "results" in root:
        continue

    for file in files:
        if file == "experiment.log":
            name = root.split("-")[-2]
            run_notebook(BOOK, f"{root}/{name}.html", path=f"{root}/")
