"""
Fabric file for automate some complex functions
"""

from fabric.api import local

DOC_VERSION = '0.0.1'


def update_the_docs():
    """
    Function to update the doc files
    """
    local('sphinx-apidoc --full -o docs esmafe '
          '-V {version} -R {version} '
          '-H Esmafe -A Guizion Labs '
          '--separate'.format(version=DOC_VERSION))
    local('make html -C docs/')


def check_pylint():
    """
    Alias to check pylint
    """
    local('pylint esmafe')
