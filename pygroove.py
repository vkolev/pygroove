#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pygroove.py
#	
#	Version: 0.1a
#
#       Copyright 2009 Vladimir Kolev <vladi@vladi-laptop>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

__author__ = "Vladimir Kolev <vladi@vladimirkolev.com"
__version__ = "0.1a"
__license__ = "BSD License"

NOLIMIT_URL = "http://tinysong.com/b/%s"
LIMIT_URL = "http://tinysong.com/s/%s?limit=%i"

import urllib
import sys

def main():
	"""
	The main method is called when pygroove.py is not used as a module

	Usage: pygroove.py -s "search term" [limit]
	-s 	--search	The term that is searched, must be placed in " "
				and the limit is an integer
	"""
	if len(sys.argv) < 2:
		usage()
	elif len(sys.argv) == 3:
		searchterm = sys.argv[2]
		print search(searchterm)
	elif len(sys.argv) == 4:
		arg = sys.argv[1]
		if arg in ('-s', '--search'):
			searchterm = sys.argv[2]
			try:
				limited = int(sys.argv[3])
				results = search(searchterm, limited)
				print results
			except ValueError:
				print "The limit must be an Integer!\n"
				usage()

		else:
			usage()
	else:
		usage()

def search(term, limit=1):
	"""
	The search method

	@type term: string
	@param term: Search term may contain " "
	@type limit: integer
	@param limit: Limit of the results
	@return: Link for song, title and singer in dictionary like {i: (Artist, Title, Link}
	@rtype: dictionary
	"""
	if limit == 1:
		if " " in term:
			term = term.replace(" ", "+")
		fullurl = NOLIMIT_URL % term
		test = urllib.urlopen(fullurl)
		result = test.read().split("; ")
		return {1: (result[0], result[4], result[2])}
	else:
		if " " in term:
			term = term.replace(" ", "+")
		fullurl = LIMIT_URL % (term, limit+1)
		request = urllib.urlopen(fullurl)
		result = request.read().split("\n")
		results = {}
		i = 1
		for song in result:
			song = song.split("; ")
			results[i] = (song[4], song[2], song[0])
			i+=1
		return results

def usage():
	print "The sumple grooveshark search tool"
	print "Usage: pygroove.py -s \"Search Term\" [limit]"
	print "	-s \t--search\tThe term that is searched, must be placed in \" \"\n\t\t\t\tand the limit is an integer"

if __name__ == "__main__":
	main()

