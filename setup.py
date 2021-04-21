from distutils.core import setup
from  setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="Myportfolio",
    version="1.0",
    packages=find_packages(),
    install_requires=required,
    entry_points = {
        "console_scripts": [
            "myportfolio=myportfolio.entrypoint:main"
            ],
    },
    license="",
    author="Vishwajeet Kaulgekar",
    long_description="Portfolio returns"
)