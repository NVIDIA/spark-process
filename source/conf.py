# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "..",
                 "pygments"),
)
import ada_pygments

def setup(app):
    app.add_lexer("ada", ada_pygments.AdaLexer)
    app.add_lexer("gpr", ada_pygments.GNATProjectLexer)


project = 'SPARK Process'
copyright = '2024-2025, NVIDIA'
author = 'NVIDIA'

GNAT_RM = "https://docs.adacore.com/R/docs/gnat-25.1/gnat_rm/html/gnat_rm/"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.extlinks"]

templates_path = ['_templates']
exclude_patterns = []
extlinks = {
    "gt" : ("https://support.adacore.com/csm?id=case&case=%s",
            "AdaCore Ticket %s"),
    "lrm" : ("http://www.ada-auth.org/standards/22rm/html/RM-%s.html",
             "Ada 2022 LRM (%s)"),
    "gnatattr" : (GNAT_RM +
                  "gnat_rm/implementation_defined_attributes.html#attribute-%s",
                  "GNAT Attribute Extension (%s)"),
}
extlinks_detect_hardcoded_links = True

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
    "logo"            : "nv_black.png",
    "description"     : "NVIDIA ISO-26262 SPARK Process",
    "show_powered_by" : False,
    "font_family"     : "NVIDIA",
}

# -- Options for LaTeX output ------------------------------------------------

latex_documents = [
    ("process/index",
     "SWE-DRIVE-249-SWTLR.tex",
     "SPARK Process",
     "NVIDIA",
     "manual",
     True),
]

latex_logo = "_static/nv_black.png"
latex_appendices = [
    "lic-gfdl",
    "bibliography"
]

# -- Options for linkcheck output --------------------------------------------

linkcheck_ignore = [
    r"https://www\.gnu\.org/*"
]
