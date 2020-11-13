
KiwiFarmer
==========

Scraping KiwiFarms threads and storing in a created MySQL database.

TODO
----

* write unit tests
* parallelize requests (possibly aiohttp)
* config file parsing
* analysis tools/utilities/visualizations
* use mysqlclient for improved performance
* improve input argument handling for classes (e.g. type conversion/checking)

Steps
-----
1. Get list of URLs for all threads
  `python get_thread_url_list.py`

2. Download the first page of each thread (rerun until all threads download successfully)
  `python download_all_threads_new.py`

3. Get list of URLs for all pages of all threads
  `python get_page_url_list.py`

4. Download all pages of all threads (rerun until all threads download successfully)
  `python download_all_pages_new.py`