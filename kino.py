#!/usr/bin/env python
# coding=utf8

import sys
import urllib2
import json
from optparse import OptionParser

# KINO_SUGGEST_URL = 'http://kino.local/suggestion.php?q='
KINO_SUGGEST_URL = 'http://10.1.5.21/suggestion.php?q='
# KINO_DETAIL_URL = 'http://kino.local/api.php?format=ajax'
KINO_DETAIL_URL = 'http://10.1.5.21/api.php?format=ajax'
PAYLOAD_TEMPLATE = 'action[0]=Video.getMovie&movie_id[0]='

def get_download_links(movie_id):
	req = urllib2.Request(KINO_DETAIL_URL, PAYLOAD_TEMPLATE + str(movie_id))
	req.add_header('Accept', 'application/json')
	res = urllib2.urlopen(req)
	data = res.read()
	response_json = data[data.index('[{"status"'):data.index(',"text":')]
	response = json.loads(response_json)
	files = response[0]['response']['movie']['files']
	# print files
	links = [f['links']['download'] for f in files if not f['is_dir']]
	return links

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-t", "--title", dest="title",
	                  help="Title of the film")
	parser.add_option("-y", "--year", dest="year", type="int", default=0,
	                  help="Minimum year")
	(options, args) = parser.parse_args()

	title = options.title.decode('utf-8')
	# print 'Searcing for [%s] movie' % title
	suggest_url = KINO_SUGGEST_URL + urllib2.quote(title.encode("utf8"))
	# create the request object and set some headers
	# print 'GET for [%s]' % suggest_url
	req = urllib2.Request(suggest_url)
	req.add_header('Accept', 'application/json')
	res = urllib2.urlopen(req)
	suggests_json = res.read()
	suggests = json.loads(suggests_json)
	# print suggests
	movies = suggests['json'][0]['response']['movies']
	# print movies
	all_links = []
	for m in movies:
		print 'name : %s, year : %s, id : %s' % (m['international_name'], m['year'], m['movie_id'])
		print m
		year_str = m['year']
		movie_year = int(year_str[year_str.index('-') + 1]) if '-' in year_str else int(year_str)
		if movie_year >= options.year:
			all_links += get_download_links(m['movie_id'])
	print '\n'.join(all_links)

