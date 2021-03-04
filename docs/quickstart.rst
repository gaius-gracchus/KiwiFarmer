
Quickstart
==========

.. _sec-quick-install:

Installation
------------

*KiwiFarmer* is not currently published through PyPi_, so to install it, first download the `source code`_, and then run the pip_ install command from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install .

To install the optional dependencies required to build the documentation for *KiwiFarmer*,  run the following command from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install .[docs]

To install the optional dependencies required to run the test suite for *KiwiFarmer*,  run the following command from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install .[tests]

.. _sec-quick-tests:

Running built-in tests
----------------------

*KiwiFarmer* is instrumented with a suite of unit tests to ensure each function and class within the package produces the expected result.
The test suite uses the pytest_ framework, and can be executed by running the following command from the *KiwiFarmer* root directory:

.. code-block:: bash

  python -m pytest

Before running the tests, the MySQL user must be granted permissions on the test database.
Log in to MySQL and open a MySQL shell by executing the following command:

.. code-block:: bash

  mysql -u root -p

wherein the user will be prompted to enter their root MySQL password. In the MySQL shell, grant privileges to the test database by executing the command:

.. code-block:: MySQL

  GRANT ALL PRIVILEGES ON kiwifarms_20210224.* TO '<user>'@'localhost';

where ``<user>`` is the user's MySQL username.

.. _sec-quick-docs:

Building the documentation
--------------------------

The documentation for *KiwiFarmer* is generated using the Sphinx_ tool, with the source files for the documentation stored as reStructuredText_ files in the ``docs`` directory.
To build the documentation in HTML format, run the following series of commands from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install . -I --no-deps   # install KiwiFarmer
  cd docs                      # change directory to docs
  rm -rf source/               # remove auto-generated documentation source code if it exists
  bash default_apidocs.sh      # run sphinx-apidoc command
  make clean                   # remove pre-built docs if they exist
  make html                    # build docs
  cd ../                       # change directory back to package root directory

or alternatively run the above series of commands in a single line from the *KiwiFarmer* package root directory:

.. code-block:: bash

  pip install . -I --no-deps && cd docs && rm -rf source/ && bash default_apidocs.sh && make clean && make html && cd ../

and view the front page of the newly built HTML website by opening the file ``docs/_build/html/index.html``.


.. _PyPi: https://pypi.org/
.. _source code: https://github.com/gaius-gracchus/KiwiFarmer
.. _pip: https://pip.pypa.io
.. _pytest: https://docs.pytest.org/en/latest/
.. _Sphinx: http://www.sphinx-doc.org
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
