#!/usr/bin/python
import sys
import urllib2, urllib

print "Send-to-patchbin tool. Usage examples: 'svn diff | sendtopatchbin'"
print "Listening on stdin..."
input_stdin = sys.stdin.read()
print "input is", input_stdin

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
	data = urllib.urlencode(postdata)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)

	try:
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
		print "Error details: ", e.message

