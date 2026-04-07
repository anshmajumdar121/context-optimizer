from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="context-optimizer",
    version="1.0.0",
    author="Context Optimizer Team",
    author_email="your.email@example.com",
    description="Reduce Claude AI token consumption by 5x-27x",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/context-optimizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Tools",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "context-mapper=tools.context_mapper:main",
        ],
    },
)
