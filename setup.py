"""Setup configuration for LADA."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8")

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = [
    line.strip() 
    for line in requirements_path.read_text().splitlines() 
    if line.strip() and not line.startswith("#")
]

setup(
    name="lada",
    version="0.1.0",
    author="Mike",
    description="Local AI-Driven Development Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ccie9658/lada",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "lada=lada.cli:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Code Generators",
    ],
)
