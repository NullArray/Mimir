#!/usr/bin/env python2.7

import pycurl
import pickle
import os.path, os, sys
import time
import StringIO
import json

from selenium import webdriver
from blessings import Terminal
from ipwhois import IPWhois
from pprint import pprint

t = Terminal()
c = pycurl.Curl()


# Check if PyCurl version supports OpenSSL, if not, rebuild.
if "OpenSSL" not in pycurl.version:
	print "\n[" + t.red("!") + "]Warning! Heuristics indicate your verion of PyCurl does not support OpenSSL."
		
	print "[" + t.green("+") + "]Detected Pycurl version: " + pycurl.version
	print "[" + t.green("+") + "]In order for Mimir to be able to connect to HoneyDB, OpenSSL is required."
		
	print "\n[" + t.magenta("?") + "]Would you like to automatically resolve this issue?"
	rebuild = raw_input("[Y]es/[N]o: ")
		
	if rebuild == 'y':
		print "\n[" + t.green("+") + "]Invoking 'rebuild.sh'...\n"
		time.sleep(1.5)
		
		try:	
			os.system("chmod +x rebuild.sh")
			os.system("./rebuild.sh")
		except Exception as e:
			print "\n[" + t.red("!") + "]Critical. An error was raised wgile attemting to invoke external utility"
			print e
			sys.exit(1)
			
		print "\n[" + t.green("+") + "]PyCurl has been rebuilt with OpenSSL support. All systems nominal."
		print "\n[" + t.green("+") + "]Mimir needs to be restarted for changes to take effect. Quitting..."
		time.sleep(2.5)
		sys.exit(1)
			
	elif rebuild == 'n':
		print "\n[" + t.green("+") + "]Not resolving."
		
	else:
		 print "\n[" + t.red("!") + "]Unhandled option. Quitting."
		 sys.exit(1)

			
		
print t.cyan("""

oooo     oooo ooooo oooo     oooo ooooo oooooooooo  
 8888o   888   888   8888o   888   888   888    888 
 88 888o8 88   888   88 888o8 88   888   888oooo88  
 88  888  88   888   88  888  88   888   888  88o   
o88o  8  o88o o888o o88o  8  o88o o888o o888o  88o8 


			    Threat Intel Interface
						   \n""")


# Check if we have API ID/key saved
if not os.path.isfile("HDB-api-ID.p"):
	
	print "[" + t.green("+") + "]Please provide your HoneyDB API ID\n"
	DB_API_ID = raw_input("API ID: ")
	
	pickle.dump(DB_API_ID, open( "HDB-api-ID.p", "wb" ))
	
	print "[" + t.green("+") + "]Please provide your HoneyDB API key\n"
	DB_API_KEY = raw_input("API key: ")
	
	pickle.dump(DB_API_KEY, open( "HDB-api-key.p", "wb" ))
	
	print "[" + t.green("+") + "]Your API data has been saved to 'HDB-api-ID.p' and 'HDB-api-key.p' in the current directory.\n"
	
else:
	
	try:
		DB_API_ID = pickle.load(open( "HDB-api-ID.p", "rb" ))
		DB_API_KEY = pickle.load(open( "HDB-api-key.p", "rb" ))
	except IOError as e:
		print "\n[" + t.red("!") + "]Critical. An IO error was raised while attempting to read API data.\n"
		print e 
		
		sys.exit(1) 
	
	ID_path = os.path.abspath("HDB-api-ID.p")
	KEY_path = os.path.abspath("HDB-api-key.p")
	
	print "\n[" + t.green("+") + "]Your API ID was succesfully loaded from " + ID_path
	print "[" + t.green("+") + "]Your API key was succesfully loaded from " + KEY_path


# WHOIS function
def whois():
	print "[" + t.green("+") + "]Please provide an IP for WHOIS lookup."
	TARGET = raw_input("\n<" + t.cyan("WHOIS") + ">$ ")
	
	obj = IPWhois(TARGET)
	results = obj.lookup_rdap(depth=1)
	pprint(results)
	
	print "\n[" + t.magenta("?") + "]Would you like to append the WHOIS record to a text file?\n"
	logs = raw_input("[Y]es/[N]o: ")
	
	format = json.dumps(results, indent = 2)
	
	if logs == "y":
		with open( "whois.log", "ab" ) as outfile:
			outfile.write("Host: " + TARGET + "\n")
			outfile.write(format)
			outfile.close()
			
		print "[" + t.green("+") + "]Results saved to whois.log in the current directory.\n"
			
	elif logs == "n":
		print "[" + t.green("+") + "]Returning to main menu.\n"
		
	else:
		print "[" + t.red("!") + "]Unhandled Option.\n"

def hosts():
	a = StringIO.StringIO()
	
	# Options for PyCurl
	opts = ['X-HoneyDb-ApiId: ' + DB_API_ID, 'X-HoneyDb-ApiKey: ' + DB_API_KEY]
	c.setopt(pycurl.HTTPHEADER, (opts))
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	
	c.setopt(pycurl.URL, "https://riskdiscovery.com/honeydb/api/bad-hosts")
	c.setopt(c.WRITEDATA, a)
	
	try:
		c.perform()
	except Exception as e:
		print "\n[" + t.red("!") + "]Critical. An error was raised with the following message"	
		print e
			
	os.system("clear")
	print "\n\n[" + t.green("+") + "]Retrieved Threat Feed, formatting..."
	time.sleep(1)
			
	response_h = json.loads(a. getvalue())
	pprint(response_h)
			
	format = json.dumps(response_h, indent = 2)

	with open('hosts.log', 'ab') as outfile:
		outfile.write(format)
		outfile.close()
				
	print "\n\nResults saved to 'hosts.log' in the current directory"

def feed():
	b = StringIO.StringIO()
	
	# Options for PyCurl
	opts = ['X-HoneyDb-ApiId: ' + DB_API_ID, 'X-HoneyDb-ApiKey: ' + DB_API_KEY]
	c.setopt(pycurl.HTTPHEADER, (opts))
	c.setopt(pycurl.FOLLOWLOCATION, 1)
			
	c.setopt(pycurl.URL, "https://riskdiscovery.com/honeydb/api/twitter-threat-feed")
	c.setopt(c.WRITEDATA, b)
	
	try:
		c.perform()
	except Exception as e:
		print "\n[" + t.red("!") + "]Critical. An error was raised with the following message"	
		print e
		
	os.system("clear")
	print "\n\n[" + t.green("+") + "]Retrieved Threat Feed, formatting..."
	time.sleep(1)
			
	response_f = json.loads(b. getvalue())
	pprint(response_f)
			
	format = json.dumps(response_f, indent = 2)

	with open('feed.log', 'ab') as outfile:
		outfile.write(format)
		outfile.close()
		
	
	print "\n\nResults saved to 'feed.log' in the current directory"

try:
	while True:

							
		print "\n\n[" + t.green("+") + "]Welcome to Mimir. Please select an action."
		print """
1. Fetch Threat Feed			5. Visualize Top Malicious Hosts in Browser
2. Fetch Bad Host List			6. Visualize Top Targeted Services in Browser
3. Perform WHOIS Lookup			7. Visualize Results for Single Host in Browser
4. Invoke Nmap Scan		        8. Quit
		
		"""		
		option = raw_input("\n<" + t.cyan("MIMIR") + ">$ ")
		
		if option == '1':
			feed()
			
		elif option =='2':
			hosts()
			
		elif option == '3':
			whois()
		
		elif option == '4':
			host = raw_input("\n[" + t.green("+") + "]Please enter a target to scan: ")
			try:
				os.system("nmap -T4 -Pn --reason " + host)
			except Exception as e:
				print "\n[" + t.red("!") + "]Critical. An error was raised with the following message "
				print e
				
		elif option == '5':
			try:
				driver = webdriver.Firefox()
				driver.get("https://riskdiscovery.com/honeydb/#hosts")
			except:
				pass
				
		elif option == '6':
			try:
				driver = webdriver.Firefox()
				driver.get("https://riskdiscovery.com/honeydb/#services")
			except:
				pass
				
		elif option == '7':
			host = raw_input("\n[" + t.green("+") + "]Please enter a host: ")
			try:
				driver = webdriver.Firefox()
				driver.get("https://riskdiscovery.com/honeydb/#host/" + host )
			except:
				pass
				
		elif option == '8':
			break
			
		else:
			print "\n[" + t.red("!") + "]Unhandled Option."

except KeyboardInterrupt:
	print "\n\n[" + t.red("!") + "]Critical. User aborted."			
