import os
import re
import time
import urllib2, urllib
import csv

import html5lib

# Limit the speed of spider requests -- delay in seconds between requests:
request_delay = 0.1

class ZipScraper(object):
    form_url = "http://zip4.usps.com/zip4/citytown_zip.jsp"
    post_url = "http://zip4.usps.com/zip4/zcl_3_results.jsp"
    user_agent = "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5"

    def __init__(self):
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [
            ('User-Agent', self.user_agent), 
            ('Referer', self.form_url),
        ]
        self.form_fields = self.get_lookup_form()

    def get_lookup_form(self):
        """ Get all the form fields required to post a zip lookup request """
        fh = self.opener.open(self.form_url)
        soup = html5lib.HTMLParser(
                tree=html5lib.treebuilders.getTreeBuilder("beautifulsoup")
            ).parse(fh)
        form = soup.find(attrs={'name': 'form1'})
        inputs = form.findAll('input')
        form_fields = {}
        for input in inputs:
            if input.has_key('name'):
                form_fields[input['name']] = input['value']
        return form_fields

    def scrape(self):
        """ Download zip code pages for every possible 5-digit zip code """
        zips = ("%05i" % i for i in range(100000))
        for zip in zips:
            self.lookup_zip(zip)
            time.sleep(request_delay)

    def lookup_zip(self, zip):
        """ Downloads and saves the USPS web site describing zip codes. """
        dest_dir = os.path.join(os.path.dirname(__file__), zip[0:2])
        dest_filename = os.path.join(dest_dir, zip + ".html")
        try:
            os.makedirs(dest_dir)
        except os.error:
            pass

        self.form_fields['zip5'] = zip
        params = urllib.urlencode(self.form_fields)
        page = self.opener.open(self.post_url, params).read()
        with open(dest_filename, 'w') as fh:
            fh.write(page)

    def collate_results(self):
        """ 
        Build a table of all zip codes, cities and states from scraped pages.
        """
        city_re = re.compile("^\s*<td.*>(?:<b>)?(\w[\w ]*), ([A-Z]{2})(?:<\/b>)?<\/td>\s*")
        not_acceptable_re = re.compile("\s*<h2.*>Not Acceptable <\/h2>\s*")
        with open("zips.csv", 'w') as fh:
            writer = csv.writer(fh)
            for zip in ("%05i" % i for i in range(100000)):
                filename = os.path.join(os.path.dirname(__file__), zip[0:2], zip + ".html")
                with open(filename) as fh:
                    print zip,
                    for line in fh:
                        if not_acceptable_re.match(line):
                            break
                        match = city_re.match(line)
                        if match:
                            city, state = match.group(1), match.group(2)
                            print (city, state),
                            writer.writerow((zip, city, state))
                    print

if __name__ == "__main__":
    scraper = ZipScraper()
    scraper.scrape()
    scraper.collate_results()
