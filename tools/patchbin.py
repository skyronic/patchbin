#!/usr/bin/env python
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
from optparse import OptionParser, OptionGroup

HEADER = """\
Patchbin upload script.
Usage examples: 'diff file1 file2 | patchbin', 'git diff | patchbin', etc.
Listening on stdin... ^C to quit"""

SUCCESS = """\
SUCCESS!! View your patch online at:

%s

Thank you for using patchbin"""

SERVER_ERROR = """\
ERROR! The server didn't seem to process your patch properly.
The exact error was:

"""

HTTP_ERROR = """\
Unable to make the HTTP Request.
Error details:"""

def _build_parser():
	"""Return a parser for the command-line interface."""
	usage = "Usage: %prog [-q]"
	parser = OptionParser(usage=usage)
	
	output = OptionGroup(parser, "Output Options")
	output.add_option("-q", "--quiet",
					  action="store_true", dest="quiet", default=False,
					  help="print only the URL of the patch")
	parser.add_option_group(output)
	
	return parser


# Craft post request and send it
if __name__ == "__main__":
	(options, args) = _build_parser().parse_args()
	
	if not options.quiet:
		print HEADER
	input_stdin = sys.stdin.read()

	name = ""
	description = "Uploaded via patchbin upload script"
	email = ""

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
			if not options.quiet:
				print SUCCESS % response.url
			else:
				print response.url,
		else:
			# The server couldn't process
			sys.stderr.write(SERVER_ERROR)
			sys.stderr.write('\n'.join(l.strip() for l in response.read().splitlines()) + '\n')
			sys.exit(1)
	except Exception, e:
		sys.stderr.write(HTTP_ERROR)
		sys.stderr.write(str(e))
		sys.exit(1)

