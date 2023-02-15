import setuptools


NAME = "datastack"
VERSION = '0.0.1'
setuptools.setup(
    name=NAME,
    version=VERSION,
    entry_points={"console_scripts":["datastack = datastack.cli:main"]},
)