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

.. |github-actions| image:: https://github.com/yusinv/priority-search-tree/actions/workflows/build.yml/badge.svg
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/yusinv/priority-search-tree/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/yusinv/priority-search-tree/compare/v0.0.1...main



.. end-badges

The priority search tree (PST) is data structure with the following properties:

* Items are stored in binary search tree (red-black tree in this case) using ``tree_key(value)``  function as a key.
* Maintains max heap properties using ``heap_key(value)`` function as key.
* Ability to perform efficient  *O(log(N)+K)* 3-sided search (finds items with ``tree_key`` in interval **[min_tree_key,max_tree_key]** and ``heap_key`` is grater or equal to **bottom_heap_key**).

For example PST can store 2 dimensional points P(X,Y) using X coordinate as ``tree_key`` and Y coordinate as ``heap_key``.  Such PST can perform 3 sided search to find points with X in [X_MIN,X_MAX] and Y >= Y_BOTTOM.

Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

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
