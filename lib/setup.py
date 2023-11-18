import setuptools
from setuptools import findall


setuptools.setup(
    name='datastack',
    version='0.0.2',
    author="Vishal Vora, Mayur Pokiya, Karan Doshi", 
    description="Tool to build data apps on the fly",
    entry_points={"console_scripts":["datastack = datastack.cli:main"]},
    install_requires=['click==8.1.3','Flask==2.2.2','Flask_Cors==3.0.10','GitPython==3.1.31','numpy','pandas',
                      'plotly==5.14.0','requests==2.28.1', 'sphinx_rtd_theme'],
    data_files=[('static', findall('datastack/static/'))],                      
    include_package_data=True,
   
)