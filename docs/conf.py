import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme

project = 'Xubuntu 20.04的配置笔记'
copyright = '2020, Taoda'
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
language = 'zh_CN'
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
