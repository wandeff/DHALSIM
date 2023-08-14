# Sphinx文档生成器的配置文件。
#
# 本文件仅包含一些最常用的选项。完整列表请参阅文档：
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- 路径设置 --------------------------------------------------------------

# 如果扩展（或要使用autodoc自动文档生成的模块）在其他目录中，
# 在此处将这些目录添加到sys.path。如果目录相对于文档根目录，则使用os.path.abspath使其绝对，如下所示。
#
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

# -- 项目信息 -----------------------------------------------------
project = 'dhalsim'
copyright = '2021, Andrés F. Murillo, Robert van Dijk, Luc Jonker, Simcha Vos, Maarten Weyns'
author = 'Andrés F. Murillo, Robert van Dijk, Luc Jonker, Simcha Vos, Maarten Weyns'

# -- 通用配置 ---------------------------------------------------
import sphinx_rtd_theme

# 在此处添加任何Sphinx扩展模块名称，作为字符串。它们可以是随Sphinx一起提供的扩展（命名为'sphinx.ext.*'）或您的自定义扩展。
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme',
    'sphinx-prompt',
    'sphinx.ext.autosectionlabel',
]

autodoc_mock_imports = ['thread', 'py2_logger', 'topo', 'basePLC', 'entities', 'automatic_node', 'minicps']

# 在此处添加包含模板的任何路径，相对于此目录。
# templates_path = ['_templates']

# 匹配文件和目录的模式列表，相对于源目录，用于在查找源文件时忽略。
# 此模式还会影响html_static_path和html_extra_path。
exclude_patterns = []

# -- HTML输出选项 -------------------------------------------------

# 用于HTML和HTML Help页面的主题。有关内置主题的列表，请参见文档。
#
html_theme = 'sphinx_rtd_theme'

# 包含自定义静态文件（例如样式表）的路径，相对于此目录。
# 在内置静态文件之后复制，因此名为"default.css"的文件将覆盖内置的"default.css"。
# html_static_path = ['_static']

# -- LaTeX输出选项 ------------------------------------------------

latex_toplevel_sectioning = 'section'

latex_elements = {
    'maketitle': r'',
    'tableofcontents': r'',
    'makeindex': r'',
    'printindex': r'',
    'fncychap': '',
}

latex_docclass = {
    'howto': 'TUD-report2020',
    'manual': 'TUD-report2020',
}

