#!/bin/bash
# get a mock evaluation, this is the data that can be used for testing
rsync -az --progress --exclude ".svn" --exclude "tmp/" data.theyworkforyou.com::parldata/scrapedxml/debates/debates2020-06-15a.xml ../xml/
# get old 1998 evaluation data
# the letters denote revision, this script downloads the latest revisions
rsync -az --progress --exclude ".svn" --exclude "tmp/" \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2016-05-09b.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2016-05-10a.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2016-05-11b.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2016-05-12a.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2016-03-11b.xml \
../xml/
# get recent 2020/21 data
rsync -az --progress --exclude ".svn" --exclude "tmp/" \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2020-12-14b.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2020-12-15a.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2020-12-16b.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2020-12-17b.xml \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2021-03-12a.xml \
../xml/