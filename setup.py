from setuptools import setup, find_packages

setup(
    name="material_fingerprinting",
    version="0.0.3", # only change this for a new release
    author="Moritz Flaschel",
    author_email="moritz.flaschel@fau.de",
    url="https://github.com/Material-Fingerprinting/material-fingerprinting",
    description="A shortcut to material model discovery without solving optimization problems.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        "material_fingerprinting": ["databases/*.npz"],
    },
    python_requires=">=3.10",
    install_requires=[
        "matplotlib",
        "numpy",
    ],
)