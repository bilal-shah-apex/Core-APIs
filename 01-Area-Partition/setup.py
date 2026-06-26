"""Setup configuration for SheetCuts package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sheetcuts",
    version="1.0.0",
    author="SheetCuts Development Team",
    description="Sheet optimization & layout engine for minimizing material wastage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sheetcuts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.14",
    install_requires=[
        # Core dependencies - minimal for maximum compatibility
        # numpy or scipy can be added in Phase 2 if benchmarks require optimization
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.0",
            "sphinx-autodoc-typehints>=1.15",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
