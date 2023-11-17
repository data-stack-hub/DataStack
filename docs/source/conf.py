# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
import sphinx.apidoc
def setup(app):
    sphinx.apidoc.main(['-f', #Overwrite existing files
                        '-T', #Create table of contents
                        #'-e', #Give modules their own pages
                        '-E', #user docstring headers
                        #'-M', #Modules first
                        '-o', #Output the files to:
                        './docs/sources/', #Output Directory
                        'lib', #Main Module directory
                        ]
    )
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'datastack'
copyright = '2023, Vishal Vora'
author = 'Vishal Vora'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
