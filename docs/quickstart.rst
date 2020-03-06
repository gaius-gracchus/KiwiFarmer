
Quickstart
==========

Installation
------------

KiwiFarmer follows the Python_ installation and distribution practices discussed in the `Python Packaging User Guide`_.
The KiwiFarmer Python package, as well as any of its Python package dependencies, can be installed by running the following command in a terminal from the KiwiFarmer package root directory:

.. code-block:: bash

  pip install .

.. _sec-quick-tests:

Running built-in tests
----------------------

KiwiFarmer is instrumented with suites of unit tests that aid in verifying the correctness of the source code.
These unit tests are implemented using Python's unittest_ framework and can be executed using:

.. code-block:: bash

  # run unit tests
  python setup.py test

The source code used to implement the unit tests is located under the ``kiwifarmer/tests`` directory.
By convention, sub-directories inside ``tests`` reflect the directory (sub-package) structure of ``kiwifarmer``.

.. _sec-quick-docs:

Building the documentation
--------------------------

The documentation for KiwiFarmer is generated using Sphinx_ tool.
Sphinx_ converts plain-text, human-readable reStructuredText_ (``*.rst``) files into HTML websites and other formats such as PDF and EPubs.
Additionally, Sphinx_ utilizes Python's native documentation facilities to auto-generate visually pleasing and easy to navigate source code documentation.
The vast majority of widely-used Python packages, including NumPy_, SciPy_, and matplotlib_, are documented using Sphinx_.

Users that modify the source code or contribute to KiwiFarmer's raw documentation files (located under the ``docs`` directory) can generate an up-to-date HTML website by executing the commands:

.. code-block:: bash

  # change current directory to be the project directory
  # cd <path to project directory>
  # the output of the ls command should be similar to:
  #   MANIFEST.in  PKG-INFO  README.rst  docs
  #   examples  kiwifarmer  kiwifarmer.egg-info  setup.cfg  setup.py

  # install/update (if necessary) sphinx and related utilities
  # required to build the documentation
  pip install .[doc]
  # change current directory to be docs
  cd docs
  # generate and modify module source files
  bash default_apidocs.sh
  # build HTML documentation
  make html

The frontpage of the newly built HTML website can be viewed by opening ``_build/html/index.html``.

Provided that the computing environment is instrumented with a LaTeX compiler and package manager, the PDF version of the documentation can be built by executing:

.. code-block:: bash

  # build PDF documentation
  make latexpdf

The final PDF file (`KiwiFarmer.pdf`) and the intermediate LaTeX_ files are located under the ``_build/latex`` directory.
Information on generating documentation files in other formats (EPubs, XML, man pages, etc.) can be found on the Sphinx_ website.

Although the Sphinx_ build system is able to automatically detect and update the documentation to reflect changes to content of existing files, it is unable to automatically take into account newly created, deleted, or renamed files and directories.
Comprehensive instructions for adding or removing files from the documentation are provided in the `Defining document structure`_ section of the Sphinx_ website.

.. _Python: https://www.python.org/
.. _pip: https://pip.pypa.io
.. _Python Packaging User Guide: https://packaging.python.org
.. _Python package: https://docs.python.org/2/tutorial/modules.html#packages
.. _unittest: https://docs.python.org/2/library/unittest.html
.. _LaTeX: https://www.latex-project.org/
.. _modules: https://docs.python.org/2/tutorial/modules.html#
.. _source distribution: https://docs.python.org/2/distutils/sourcedist.html#
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://www.sphinx-doc.org
.. _setuptools: https://setuptools.readthedocs.io
.. _NumPy: http://www.numpy.org/
.. _SciPy: https://www.scipy.org/
.. _matplotlib: https://matplotlib.org/
.. _Defining document structure: https://www.sphinx-doc.org/en/master/usage/quickstart.html#defining-document-structure