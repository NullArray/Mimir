# Mimir
OSINT Threat Intel Interface

Named after the old Norse God of knowledge.

## About
I had the idea to write an OSINT Threat Intel tool that functions as a CLI to HoneyDB if you don't know what HoneyDB is. It's a sort of aggregative open source intelligence platform. Basically it collects a bunch of info from HoneyPy Honeypots in order to learn about malicious hosts, top attacked services and more. More information [here](https://riskdiscovery.com/honeydb/#about). 

The idea of my tool is to make it easier for the pentester/researcher/InfoSec pro to access this information and do something meaningful with it. To that end i have included in script WHOIS lookup and the ability to invoke an Nmap scan on a provided host.

## Active Development & Known issue
With the API we are able to retrieve the threat feed and bad host list as well. The program would allow you to retrieve this data easily and save it for further processing and/or investigation. But herein lies a problem. The project is written in Python 2.7, the built in SSL lib in Python 2.7 does not support the SSL version HoneyDB runs. And as far as i can see there isn't a particularly viable work-around. I have the full source posted in the repo and have commented out the monkey patch i have tried, it attempts to overwrite some functionality of the SSL lib but unfortunately i have been unable to get it to work properly.

I figured since the end product would be open source i might as well post the project as is and hopefully open source a solution to this problem as well.

### Note
Since the program depends on a lot of external modules using tools like 2to3 seems inviable, also because there is no equivalent that i know of for Mechanize in Python 3.

For clarity here are the dependencies.

```
Blessings
ipwhois
Mechanize
Selenium (For data visualization in a browser environment)
pprint
```
If you're interested in the devlopment of this tool i would encourage you to submit [a pull request](https://github.com/NullArray/Mimir/pulls) or suggestion [by opening a ticket](https://github.com/NullArray/Mimir/issues).

Thanks.
