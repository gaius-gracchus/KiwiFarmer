
Quickstart
==========

.. _sec-quick-install:

Installation
------------

*KiwiFarmer* is not currently published through PyPi_, so to install it, first download the `source code`_, and then run the pip_ install command from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install .

.. _sec-quick-tests:

Running built-in tests
----------------------

*KiwiFarmer* is instrumented with a suite of unit tests to ensure each function and class within the package produces the expected result.
The test suite uses the unittest_ framework, and can be executed by running the following command from the *KiwiFarmer* root directory:

.. code-block:: bash

  python setup.py test

.. _sec-quick-docs:

Building the documentation
--------------------------

The documentation for *KiwiFarmer* is generated using the Sphinx_ tool, with the source files for the documentation stored as reStructuredText_ files in the ``docs`` directory.
To build the documentation in HTML format, run the following command from the ``docs`` directory:

.. code-block:: bash

  make html

and view the front page of the newly built HTML website by opening the file ``_build/html/index.html``.


.. _PyPi: https://pypi.org/
.. _source code: https://github.com/gaius-gracchus/KiwiFarmer
.. _pip: https://pip.pypa.io
.. _unittest: https://docs.python.org/3/library/unittest.html
.. _Sphinx: http://www.sphinx-doc.org
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
