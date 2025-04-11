# Installation

## Execution environment

There are two main constraints with regards to the execution environment.
These are that it must run on Linux/Unix and the Python version must be `>=3.8` and `<=3.10`.
This app was developed using Python version 3.9.

### Python constraint

Python must be `>=3.8` and `<=3.10`.
This to accommodate the `numpy` version required by `pbcore`.
Pre-built distributions of `numpy==1.22.4` are only available for Python 3.8-3.10.

### Linux/Unix constraint

Run on Linux/Unix.
This is because there are no pre-built distributions of `pysam` (a dependency of `pbcore`) available for Windows.

## Set up venv

Set up the virtual python environment using a supported (see above) python version.
Use `python -m venv venv` to create the virtual environment, followed by `pip install -r requirements.txt` to install all required packages.

## Troubleshooting

**Problem:** I'm building the virtual environment and pip is trying and failing to build packages.

**Solution:** This is a very generic Python issue.
The basic problem is that a pre-built version of this package is not available.
Availability of pre-built packages (a.k.a. "wheels") depends on your operating system and Python version.