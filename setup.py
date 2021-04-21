from distutils.core import setup
from  setuptools import setup, find_packages

setup(
    name="Myportfolio",
    version="1.0",
    packages=find_packages(),
    entry_points = {
        "console_scripts": [
            "myportfolio=myportfolio.entrypoint:main"
            ],
    },
    license="",
    author="Vishwajeet Kaulgekar",
    long_description="Portfolio returns"
)