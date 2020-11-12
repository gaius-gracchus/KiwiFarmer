
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
1. Get list of all threads
  `python get_url_list.py`

2. Download the first page of each thread
  `python download_all_threads.py`
