from setuptools import setup, find_packages

setup(
    name="calculator",
    version="0.1.0",
    description="iOS-style CLI calculator with beautiful interface",
    author="Claude",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "calculator=cli.main:main",
        ],
    },
)
