
KiwiFarmer
==========

KiwiFarmer is a Python package for scraping KiwiFarms threads and posts, extracting field values, and storing the results in a created MySQL database.

TODO
----

* make function and class input keyword arguments make more sense and be more consistent

* expand unit tests

  * verify correctness of functions

  * test utils

  * add function tests for new functions (e.g. reactions)

* expand instructions and info of docs

* make sick logo/favicon

* config file parsing

* analysis tools/utilities/visualizations

* use mysqlclient for improved performance

* improve input argument handling for classes (e.g. type conversion/checking)


Steps
-----
1. Get list of URLs for all threads

  .. code-block:: bash

    python get_thread_url_list.py

2. Download the first page of each thread (rerun until all threads download successfully)

  .. code-block:: bash

    python download_all_threads_new.py

3. Get list of URLs for all pages of all threads

  .. code-block:: bash

    python get_page_url_list.py

4. Download all pages of all threads (rerun until all pages download successfully)

  .. code-block:: bash

    python download_all_pages_new.py