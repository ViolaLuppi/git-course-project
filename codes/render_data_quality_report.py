#--------------
# 1. Settings 
#--------------

import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

# -------------------
# 2. Directories
#--------------------
# PROJECT_DIR is the root of the project (assumes this script is run from there)
# REPORT_PATH points to the Quarto markdown file (.qmd) to be rendered
# OUTPUT_DIR  is where the rendered HTML report will be saved; created if absent

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_DIR / "codes" / "data_quality_report.qmd"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Rendering the Quarto quality report...")


#-----------------
# 3. Locate Quarto
#-----------------

# shutil.which() searches the system PATH for the quarto executable,
# the same way a terminal would. On Windows with a standard Quarto install
# this is usually enough. It returns None if nothing is found.

quarto = shutil.which("quarto")

if quarto is None:
    common_paths = [
        Path.home() / "AppData" / "Local" / "Programs" / "Positron" / "resources" / "app" / "quarto" / "bin" / "quarto.cmd",
        Path.home() / "AppData" / "Local" / "Programs" / "Quarto" / "bin" / "quarto.cmd",
        Path("/usr/local/bin/quarto"),
        Path("/opt/quarto/bin/quarto"),
    ]
    for path in common_paths:
        if path.exists():
            quarto = str(path)
            break

if quarto is None:
    raise RuntimeError(
        "Quarto was not found. Install it from https://quarto.org/docs/get-started/ "
        "or add it to your PATH."
    )

print("Quarto executable:", quarto)
print("Python executable:", sys.executable)

#-----------------------
# 4. Python environment 
#-----------------------

# Quarto looks for a "python3" binary by default, which does not exist on
# Windows. Setting QUARTO_PYTHON to sys.executable tells Quarto to use the
# exact Python binary that is running this script, which also guarantees that
# all packages installed in the current environment are available inside the
# .qmd code cells.

env = os.environ.copy()
env["QUARTO_PYTHON"] = sys.executable

#-----------
# 5. Render
#-----------
result = subprocess.run(
    [quarto, "render", str(REPORT_PATH), "--to", "html",
     "--output-dir", str(OUTPUT_DIR)],
    cwd=PROJECT_DIR,
    capture_output=True,
    text=True,
    env=env
)

#----------------
# Report outcome 
#----------------

print("── Quarto stdout ──────────────────────────────")
print(result.stdout)
print("── Quarto stderr ──────────────────────────────")
print(result.stderr)
print("Return code:", result.returncode)

if result.returncode != 0:
    print("Quarto render failed — see output above for details.")
else:
    # Quarto mirrors the source structure, so the HTML lands in output/codes/
    html_output = OUTPUT_DIR / "codes" / REPORT_PATH.with_suffix(".html").name
    print("Quality report rendered successfully!")
    print(f"Opening report: {html_output}")
    webbrowser.open(html_output.as_uri())