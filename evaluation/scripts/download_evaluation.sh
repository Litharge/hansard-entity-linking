#!/bin/bash
# get five test days, letters chosen so that only the most updated revision is fetched
rsync -az --progress --exclude ".svn" --exclude "tmp/" \
data.theyworkforyou.com::parldata/scrapedxml/debates/debates2020-06-15a.xml \
../xml/