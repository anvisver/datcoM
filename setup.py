from setuptools import setup, find_packages
from pathlib import Path

# Leer README.md (aunque esté vacío, no rompe)
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Leer la versión desde version.py
version = {}
with open("datcoM/version.py") as f:
    exec(f.read(), version)

setup(
    name="datcoM",
    version=version["__version__"],
    packages=find_packages(),          # Encuentra automáticamente datcoM y subpaquetes
    include_package_data=True,
    description="Paquete datcoM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Envisver",
    python_requires=">=3.7",
)
