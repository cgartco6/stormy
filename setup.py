from setuptools import setup, find_packages

setup(
    name="stormy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "stormy = main:cli_main",
        ],
    },
)
