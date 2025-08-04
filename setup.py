from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hrm-hierarchical-reasoning-machine",
    version="0.4.0",  # 40% completion - proof of concept
    author="HRM Implementation Team",
    author_email="contact@hrm-project.org",
    description="Hierarchical Reasoning Machine with MCP Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/hrm-hierarchical-reasoning-machine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",  # Proof of concept
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS :: MacOS X",  # Developed on Mac Mini
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0", 
            "black>=22.0.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.5.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "ml": [
            "scikit-learn>=1.1.0",
            "torch>=1.12.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "hrm-demo=examples.hrm_examples:main",
        ],
    },
    keywords="hierarchical reasoning artificial intelligence mcp claude",
    project_urls={
        "Bug Reports": "https://github.com/your-username/hrm-hierarchical-reasoning-machine/issues",
        "Source": "https://github.com/your-username/hrm-hierarchical-reasoning-machine",
        "Documentation": "https://hrm-hierarchical-reasoning-machine.readthedocs.io/",
    },
)
