import os
import sys

sys.path.insert(0, os.path.abspath('../src'))


project = 'proyecto_app'
copyright = '2026, Mara D.Levroni C.'
author = 'Mara D.Levroni C.'
release = '0.1'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'


html_theme = 'sphinx_rtd_theme'


html_static_path = ['_static']


html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'titles_only': False,
}
