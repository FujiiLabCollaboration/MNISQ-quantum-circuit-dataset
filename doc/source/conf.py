# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "qulacs_dataset"
copyright = "2021, Qulacs-Osaka"
author = "Qulacs-Osaka"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_nb",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

html_theme_options = {
    "repository_url": f"https://github.com/{author}/python-project-template",
    "repository_branch": "main",
    "use_repository_button": True,
    "path_to_docs": "doc/source",
    "launch_buttons": {"colab_url": "https://colab.research.google.com"},
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Some notebooks take too long time to wait for finishing in documentation build.
# For these cases, notebooks execution can be turned off.
# c.f. https://myst-nb.readthedocs.io/en/latest/computation/execute.html#notebook-execution-modes
# nb_execution_mode = "off"

# Since myst_nb==0.14.0, the dollarmath syntax extension is no longer included by default.
# So enable here explicitly.
myst_enable_extensions = ["dollarmath"]
