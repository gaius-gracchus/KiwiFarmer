
KiwiFarmer
==========

KiwiFarmer is a Python package for scraping KiwiFarms threads and posts, extracting field values, and storing the results in a created MySQL database.

TODO
----

* add additional user fields for user signature and location

* expand unit tests

  * verify correctness of functions

* expand instructions and info of docs

* config file parsing

* analysis tools/utilities/visualizations

* improve input argument handling for classes (e.g. type conversion/checking)


Workflow
--------

KiwiFarmer includes scripts for a workflow that downloads all website pages as HTML files, extracts relevant field data, and stores the data in a MySQL database.
These scripts are in the `workflow/` subdirectory in the package root directory.
For more information, see `docs/workflow.rst`