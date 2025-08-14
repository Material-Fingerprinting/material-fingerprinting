from setuptools import setup, find_packages

setup(
    name="material_fingerprinting",
    version="0.0.2",
    author="Moritz Flaschel",
    author_email="moritz.flaschel@fau.de",
    url="https://github.com/Material-Fingerprinting",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        "material_fingerprinting": ["databases/*.npz"],
    },
    install_requires=[
        "matplotlib",
        "numpy",
    ],
)