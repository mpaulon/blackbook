import json

from pathlib import Path

import black
import black.report

def blackbook(notebook:Path):
    with open(notebook) as nb:
        nb_json = json.load(nb)
        for i, cell in enumerate(nb_json.get("cells")):
            if cell.get("cell_type") != "code":
                continue
            current_code = "".join(cell.get("source"))
            try:
                new_code = black.format_cell(current_code, fast=False, mode=black.FileMode())
            except black.report.NothingChanged:
                continue
            nb_json["cells"][i]["source"] = new_code.splitlines(True)
        
        output_notebook = notebook.parent / f"fixed_{notebook.name}"

        with open(output_notebook, "w") as fixed_nb:
            fixed_nb.write(json.dumps(nb_json, indent=4))

def cli():
    import argparse
    parser = argparse.ArgumentParser("blackbook")
    parser.add_argument("notebook", type=Path)
    args = parser.parse_args()
    blackbook(args.notebook)

if __name__ == "__main__":
    cli()