========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |github-actions| |codecov|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/priority-search-tree/badge/?style=flat
    :target: https://readthedocs.org/projects/priority-search-tree/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/yusinv/priority-search-tree/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/yusinv/priority-search-tree/actions

.. |codecov| image:: https://codecov.io/gh/yusinv/priority-search-tree/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/yusinv/priority-search-tree

.. |version| image:: https://img.shields.io/pypi/v/priority-search-tree.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/priority-search-tree

.. |wheel| image:: https://img.shields.io/pypi/wheel/priority-search-tree.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/priority-search-tree

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/priority-search-tree.svg
    :alt: Supported versions
    :target: https://pypi.org/project/priority-search-tree

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/priority-search-tree.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/priority-search-tree

.. |commits-since| image:: https://img.shields.io/github/commits-since/yusinv/priority-search-tree/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/yusinv/priority-search-tree/compare/v0.0.0...main



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install priority-search-tree

You can also install the in-development version with::

    pip install https://github.com/yusinv/priority-search-tree/archive/main.zip


Documentation
=============


https://priority-search-tree.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
