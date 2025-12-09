from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="egrading-api",
    version="0.1.0",
    author="Aferiad Kamal",
    author_email="kamal@aferiad.xyz",
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NacreousDawn596/egrading-api",
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "urllib3",
        "g4f",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
