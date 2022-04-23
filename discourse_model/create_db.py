import csv
import sqlite3

from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import time
from bs4 import BeautifulSoup

class MPData:
    def __init__(self, mp_url=None, constituency=None, party=None, dummy_mp=False):
        #self.name = mp_name
        self.offices = []

        mp_html = self.fetch_html_for_mp(mp_url)
        mp_soup = BeautifulSoup(mp_html, "html.parser")

        self.constituency = constituency
        self.party = party
        self.set_offices(mp_soup)




    def set_offices(self, mp_soup):
        offices_heading = mp_soup.find(string="Currently held offices")
        #print(offices_heading)
        #print("sib 1")

        if offices_heading is None:
            self.offices = None
            return

        offices_heading_parent = offices_heading.parent

        offices_ul = offices_heading_parent.find_next_sibling("ul")

        # finds all tags containing the duration of the item
        lis = offices_ul.find_all("small")
        # name of the office is the text that is the previous sibling to the duration tag
        for li in lis:
            self.offices.append(li.previous_sibling.rstrip())


    def fetch_html_for_mp(self, url, retry_duration_seconds=3, request_timeout_seconds=5):
        correct_endpoint_prefix = "https://www.theyworkforyou.com/mp/"
        print("url: ", url)

        mp_endpoint = url

        while True:
            try:
                with urlopen(mp_endpoint, timeout=request_timeout_seconds) as response:
                    mp_html = response.read()
            except HTTPError as e:
                print(e.code)
                time.sleep(retry_duration_seconds)
            except URLError as e:
                print(e.reason)
                time.sleep(retry_duration_seconds)
            else:
                print("success on ", mp_endpoint)
                break

        return mp_html


def insert_into_db(mp):
    print(mp.party)
    print(mp.constituency)
    print(mp.offices)
    # todo: insert MP data into DB
    #conn = sqlite3.connect(db_location)



def create_db_from_list(list_file, db_location):
    with open(list_file, "r") as f:
        decoded = f.read()

    cr = csv.reader(decoded.splitlines(), delimiter=",")
    mp_list = list(cr)

    # skip first row
    for row in mp_list[1:]:
        party = row[3]
        constituency = row[4]
        url = row[5]

        print("url1", url)

        mp = MPData(mp_url=url, constituency=constituency, party=party)

        insert_into_db(mp)