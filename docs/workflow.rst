
Workflow
========

KiwiFarmer includes scripts for a workflow that downloads all website pages as HTML files, extracts relevant field data, and stores the data in a MySQL database.
These scripts are in the `workflow/` subdirectory in the package root directory.
The scripts are (to be run in order):

1. Get thread data

  A. Get list of URLs for all threads

    .. code-block:: none

      python 01-A_get_thread_url_list.py

  B. Download the first page of each thread

    .. code-block:: none

      python 01-B_download_all_threads_new.py

  C. Insert data from all threads into database

    .. code-block:: none

      python 01-C_insert_threads.py

2. Get post data

  A. Get list of URLs for all pages of all threads

    .. code-block:: none

      python 02-A_get_page_url_list.py

  B. Download all pages of all threads

    .. code-block:: none

      python 02-B_download_all_pages.py

  C. Insert data from all posts into database

    .. code-block:: none

      python 02-C_insert_pages.py

3. Get user data

  A. Download all pages of users

    .. code-block:: none

      python 03-A_download_all_users.py

  B. Insert data from all users into database

    .. code-block:: none

      python 03-B_insert_users.py

4. Get user following data

  A. Download all "About" pages of users

    .. code-block:: none

      python 04-A_download_all_users_about.py

  B. Get list of URLs for all following pages of all users

    .. code-block:: none

      python 04-B_insert_users.py

  C. Download following pages of all users

    .. code-block:: none

      python 04-C_download_all_users_following.py

  D. Insert all user following data into database

    .. code-block:: none

      python 04-D_insert_following.py

5. Get user trophy data

  A. Insert all user trophy data into database

    .. code-block:: none

      python 05-A_insert_trophies.py

6. Get reaction data

  A. Get list of URLs for reactions to all posts

    .. code-block:: none

      python 06-A_get_reaction_url_list.py

  B. Download reactions to all posts

    .. code-block:: none

      python 06-B_download_all_reactions.py

  C. Insert data from all reactions into database

    .. code-block:: none

      python 06-C_insert_reactions.py