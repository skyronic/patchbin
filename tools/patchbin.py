#!/usr/bin/python
# Copyright (c) 2010 Anirudh Sanjeev <anirudh@anirudhsanjeev.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import urllib2, urllib

print "Patchbin upload script. Usage examples: 'diff file1 file2|patchbin', 'git\
diff | patchbin', etc."
print "Listening on stdin... ^C to quit"
input_stdin = sys.stdin.read()

name = ""
description = "Uploaded via patchbin upload script"
email = ""

# Craft post request and send it
if __name__ == "__main__":
	url = "http://patchbin.com/submit"
	postdata = {
			'patchText':input_stdin,
			'authorName':name,
			'authorEmail':email,
			'patchDesc':description
			}
	try:
		data = urllib.urlencode(postdata)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)

		if(response.url != url):
			# Completed successfully
			print "SUCCESS!! View your patch online at:\n\n" + response.url + "\n\n"
			print "Thank you for using patchbin"
		else:
			# The server couldn't process
			print "ERROR! The server didn't seem to process your patch properly. The exact error was"
			print response.read()
	except Exception, e:
		print "Unable to make the HTTP Request."
		print "Error details: ", e

