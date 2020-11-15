
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
The test suite uses the pytest_ framework, and can be executed by running the following command from the *KiwiFarmer* root directory:

.. code-block:: bash

  python -m pytest

.. _sec-quick-docs:

Building the documentation
--------------------------

The documentation for *KiwiFarmer* is generated using the Sphinx_ tool, with the source files for the documentation stored as reStructuredText_ files in the ``docs`` directory.
To build the documentation in HTML format, run the following series of commands from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install . -I --no-deps   # install KiwiFarmer
  cd docs                      # change directory to docs
  rm -rf source/               # remove auto-generated documentation source code if it exists
  bash default_apidocs.sh      # run sphinx apidoc command
  make clean                   # remove pre-build docs if they exist
  make html                    # build docs
  cd ../                       # change directory back to package root directory

or alternatively run the above series of commands in a single line from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install . -I --no-deps && cd docs && rm -rf source/ && bash default_apidocs.sh && make clean && make html && cd ../

and view the front page of the newly built HTML website by opening the file ``_build/html/index.html``.


.. _PyPi: https://pypi.org/
.. _source code: https://github.com/gaius-gracchus/KiwiFarmer
.. _pip: https://pip.pypa.io
.. _pytest: https://docs.pytest.org/en/latest/
.. _Sphinx: http://www.sphinx-doc.org
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
