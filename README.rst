getzips
=======

``getzips`` is a simple project to get an up-to-date list of all zip codes with
corresponding cities and states from publicly available sources on the internet
(specifically, the USPS website).  It operates by downloading (or "spidering")
the response pages for the `USPS zip code search
<http://zip4.usps.com/zip4/citytown_zip.jsp>`_ for all possible 5-digit codes
(00000 to 99999).  The pages are then parsed to extract city and state
information.

Recent spidering results are contained in ``zips.csv``.  If you run this script
and obtain more current results, please submit a pull request with the updated
data.

usage
-----

To run your own spidering operation:

    $ python spider_usps.py

Please note that this will take some time (probably more than 24 hours,
depending on the speed of your computer and Internet connection).  The script
limits the speed of its requests using the ``request_delay`` variable (set at
the top of the script), in order to play nice with USPS.
