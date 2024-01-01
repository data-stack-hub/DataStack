import setuptools
from setuptools import findall
from distutils.core import setup

setuptools.setup(
    name="pydatastack",
    version="0.0.13",
    author="Vishal Vora, Mayur Pokiya, Karan Doshi",
    description="The Fastes way to build apps in python",
    long_description_content_type="text/markdown",
    long_description="Datastack package",
    entry_points={"console_scripts": ["datastack = datastack.cli:main"]},
    install_requires=[
        "click==8.1.3",
        "Flask==2.2.2",
        "Flask_Cors==3.0.10",
        "GitPython==3.1.31",
        "numpy",
        "pandas",
        "plotly==5.14.0",
        "requests==2.28.1",
        "cachetools",
        "varname",
        "asttokens",
        "pure_eval",
        "Werkzeug==2.2.2",
        "waitress",
        "gunicorn; sys_platform == 'linux'",
        "docutils",
        "docstring_parser",
        "numpydoc",
    ],
    data_files=[("static", findall("datastack/static/"))],
    include_package_data=True,
    setup_requires=["wheel"],
)
