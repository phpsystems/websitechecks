#!/usr/bin/env python

''' 
Script to check for the presence of HPKP headers and alert if incorrect

More info:
https://scotthelme.co.uk/guidance-on-setting-up-hpkp/
https://blog.qualys.com/ssllabs/2016/09/06/is-http-public-key-pinning-dead
'''

import optparse
import mechanize

def checkerHeader(header, check, debug):
	if (debug):
		if (len(header.getheaders('Public-Key-Pins')) > 0):
			print "[+] HPKP Header: Header not Empty"
			print "[+] HPKP Header: Rows " + str(len(header.getheaders('Public-Key-Pins')))
			print "[+] HPKP Header: " + str(header.getheaders('Public-Key-Pins')[0])
			if check is not None:
				print "[+] HPKP Header: Comparing header with " + check
		else:
			print "[+] HPKP Header: Header is empty"
			
	if  len(header.getheaders('Public-Key-Pins')) == 0:
		return (False, False)
	elif  header.getheaders('Public-Key-Pins')[0] == check:
		return (True, True)
	else:
		return (True, False)

                        
def viewPage(url, agent, debug):
	if ((url.startswith("http://") == False) and (url.startswith("https://") == False)):
		url = "https://" + url	

	if (debug):
		print "[+] Browsing : "  +url.strip() +" As " + agent.strip()

	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.addheaders = [('User-agent',agent)]
	browser.addheaders = [('Accept','test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
	browser.set_handle_refresh(False)
	        
        try:
		page = browser.open(url.strip())
		if (debug):
			print "[+] Response Code: " +str(page.code)
			
		return page.info()
	finally:
		return page.info()
		
		
def main():

	# Options for the script
	parser = optparse.OptionParser('Usage %prog% ' + " -u <url> -a <agent>")
        parser.add_option('-u', dest='url', type='string', help='Specify the URL')	
	parser.add_option('-a', dest='agent', type='string', help='Specify the user agent')
	parser.add_option('-c', dest='header', type='string', help='Specify the HSTS to check against')
	parser.add_option('-d', dest='debug', action="store_true", default=False, help='Debug Mode')
	
	(options, args) = parser.parse_args()
	
		
	if (options.url == None):
		print parser.usage
		exit(0)
	if (options.agent == None):
		if (options.debug):
			print "[-] No Useragent Set. Defaulting to Mozilla"
		options.agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"	
	
	header = viewPage(options.url, options.agent, options.debug)
	(hpkp,checked) = checkerHeader(header, options.header, options.debug)

	if (hpkp):
		print "[-] HPKP header is present"
		if (checked):
			print "[+] Header is ok"
			exit(0)
		else:
			print "[-] Header is not correct"
			exit(1)
	else:		
		print "[+] HPKP header is not present"
		exit(0)
		
		
if __name__ == '__main__':

        main()
        
