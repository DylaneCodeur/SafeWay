"""
Setup script for SafeWay
Réalisé par dylanecodeur
Created by dylanecodeur
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="safeway",
    version="1.0.0",
    author="dylanecodeur",
    author_email="",
    description="AI-powered driver assistance system for fatigue and distraction detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylanecodeur/SafeWay",
    packages=find_packages(where="safeway"),
    package_dir={"": "safeway"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.0",
        "numpy>=1.24.0,<2.0.0",
        "ultralytics>=8.0.0",
        "playsound==1.2.2",
        "pygame>=2.5.0",
        "pyttsx3>=2.90",
        "numba>=0.58.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "training": [
            "labelImg>=1.8.6",
        ],
    },
    entry_points={
        "console_scripts": [
            "safeway=safeway.ui.cli_demo:main",
        ],
    },
)

