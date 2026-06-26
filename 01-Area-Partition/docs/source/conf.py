"""Sphinx configuration file for SheetCuts documentation.

Generated docs with: sphinx-build -b html docs/source docs/build/
Output location: docs/build/html/index.html
"""

import os
import sys

# Add source to path so autodoc can find modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

project = 'SheetCuts'
copyright = '2026, SheetCuts Development Team'
author = 'SheetCuts Development Team'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',           # Auto-extract docstrings from code
    'sphinx.ext.autodoc.typehints', # Include type hints in documentation
    'sphinx.ext.napoleon',           # Parse Google-style docstrings
    'sphinx.ext.viewcode',           # Link to source code
]

# Napoleon extension settings (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_typehints = "description"   # Show hints in descriptions
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': False,
    'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
}

html_static_path = ['_static']

# Sphinx version check
needs_sphinx = '5.0'
