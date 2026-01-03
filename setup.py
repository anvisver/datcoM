# setup.py
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="datcoM",
    version="5.1",  # <- poner la versión directamente aquí
    packages=find_packages(),
    include_package_data=True,
    description="Paquete datcoM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Envisver",
    python_requires=">=3.7",
)
