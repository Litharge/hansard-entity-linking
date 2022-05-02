import csv
import sqlite3
import pickle

from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import time
from bs4 import BeautifulSoup

import datetime

import os
import os.path

# TODO: add id's, precompute shadow status, secretarial status, ministerial status, speaker status, deputy speaker status

class MPData:
    def __str__(self):
        representation = f"{self.url} \n {self.first_name} {self.last_name} \n {self.constituency} {self.party} \n {self.current_offices} \n {self.past_offices}"

        return representation


    def __init__(self, mp_url=None, constituency=None, party=None, first_name=None, last_name=None, dummy_mp=False):
        #self.name = mp_name
        self.offices = []

        mp_html = self.fetch_html_for_mp(mp_url)
        mp_soup = BeautifulSoup(mp_html, "html.parser")

        self.url = mp_url

        # dictionary where key is office, value is datetime
        self.current_offices = {}
        # dictionary where key is office, value is tuple of start and end datetime
        self.past_offices = {}

        self.constituency = constituency
        self.party = party
        self.first_name = first_name
        self.last_name = last_name

        self.set_current_offices(mp_soup)
        self.set_historical_offices(mp_soup)




    def set_current_offices(self, mp_soup):
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
            office_name = li.previous_sibling.rstrip()
            right = li.text.split("(since ")[1]
            date_text = right.split(")")[0]
            print(f"\'{date_text}\'")
            datetime_for_start = datetime.datetime.strptime(date_text, "%d %b %Y")
            print(datetime_for_start)

            self.current_offices[office_name] = datetime_for_start


    def set_historical_offices(self, mp_soup):
        offices_heading = mp_soup.find(string="Other offices held in the past")

        if offices_heading is None:
            print("skipping")
            self.offices = None
            return

        offices_heading_parent = offices_heading.parent

        offices_ul = offices_heading_parent.find_next_sibling("ul")

        # finds all tags containing the duration of the item
        lis = offices_ul.find_all("small")
        # name of the office is the text that is the previous sibling to the duration tag
        for li in lis:
            office_name = li.previous_sibling.rstrip()
            right = li.text.split("(")[1]
            mid = right.split(")")[0]

            start_end = mid.split(" to ")


            datetime_for_start = datetime.datetime.strptime(start_end[0], "%d %b %Y")
            datetime_for_end = datetime.datetime.strptime(start_end[1], "%d %b %Y")

            self.past_offices[office_name] = (datetime_for_start, datetime_for_end)


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



class MPList():
    def __init__(self, list_file=None, directory=None, date=None, create_pickle=True):
        if create_pickle:
            self.mp_list = []
            self.create_pickle_from_list(list_file, directory, date)

    def create_pickle_from_list(self, list_file, directory, date):
        with open(list_file, "r") as f:
            decoded = f.read()

        cr = csv.reader(decoded.splitlines(), delimiter=",")
        mp_list = list(cr)

        # skip first row
        for row in mp_list[1:]:
            first_name = row[1]
            last_name = row[2]
            party = row[3]
            constituency = row[4]
            url = row[5]

            mp = MPData(mp_url=url, constituency=constituency, party=party, first_name=first_name, last_name=last_name)

            self.mp_list.append(mp)

        pickle.dump(self, open(directory + date + ".p", "wb"))