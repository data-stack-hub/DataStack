import setuptools
from setuptools import findall


setuptools.setup(
    name='datastack',
    version='0.0.1',
    author="Vishal Vora, Mayur Pokiya, Karan Doshi", 
    description="Tool to build data apps on the fly",
    entry_points={"console_scripts":["datastack = datastack.cli:main"]},
    install_requires=['click==8.1.3','Flask==2.2.2','Flask_Cors==3.0.10','GitPython==3.1.31','numpy==1.24.1','pandas==2.0.0',
                      'plotly==5.14.0','requests==2.28.1','setuptools==67.7.0'],
    data_files=[('datastack/static', findall('static/'))],                      
    include_package_data=True,
   
)