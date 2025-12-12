from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nfl-occi",
    version="0.1.0",
    author="NFL OCCI Team",
    description="Offensive Conflict Creation Index for NFL teams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "nfl_data_py>=0.3.0",
        "flask>=3.0.0",
        "plotly>=5.17.0",
    ],
)
