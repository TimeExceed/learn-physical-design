import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme

project = 'EDA物理设计学习笔记'
author = 'Taoda'

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.graphviz',
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinx.ext.todo',
]
autosectionlabel_prefix_document = True
todo_include_todos = True
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_extra_path = ['_extra']
