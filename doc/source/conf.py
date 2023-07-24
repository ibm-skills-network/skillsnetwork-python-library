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
import sys
import skillsnetwork

from operator import attrgetter
from os.path import relpath
from inspect import getsourcefile, getsourcelines
from pathlib import Path

sys.path.insert(0, Path(__file__).parents[2].resolve().as_posix())


# -- Project information -----------------------------------------------------

project = "skillsnetwork"
copyright = "2022, Bradley Steinfeld, Sam Prokopchuk, James Reeve"
author = "Bradley Steinfeld, Sam Prokopchuk, James Reeve"

# The full version, including alpha/beta/rc tags
release = "0.20.6"


# -- General configuration ---------------------------------------------------
autosummary_imported_members = True

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx_autodoc_typehints",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# The path to the favicon icon
html_favicon = "_static/SN_favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_theme_options = {
    "logo": {
        "image_light": "SN_web_lightmode.png",
        "image_dark": "SN_web_darkmode.png",
    }
}


# -- Options for the linkcode extension --------------------------------------
# Resolve function
# This function is used to populate the (source) links in the API
def linkcode_resolve(domain, info):
    if domain != "py" or not info["module"] == "skillsnetwork":
        return None
    try:
        obj = attrgetter(info["fullname"])(skillsnetwork)
        fn = relpath(
            getsourcefile(obj),
            start=Path(skillsnetwork.__file__).parent,
        )
        source, lineno = getsourcelines(obj)
        fpath = f"skillsnetwork/{fn}#L{lineno}-L{lineno + len(source) - 1}"
    except Exception as e:
        return None
    import subprocess

    commit_hash = subprocess.Popen(
        ["git", "rev-parse", "HEAD"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    ).communicate()[0][:-1]
    return f"https://github.com/ibm-skills-network/skillsnetwork-python-library/blob/{commit_hash}/{fpath}"
