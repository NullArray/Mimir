# Mimir
OSINT Threat Intel Interface - Named after the old Norse God of knowledge.

I had the idea to write an OSINT Threat Intel tool that functions as a CLI to HoneyDB if you don't know what HoneyDB is. It's a sort of aggregative open source intelligence platform. Basically it collects a bunch of info from HoneyPy Honeypots in order to learn about malicious hosts, top attacked services and more. More information [here](https://riskdiscovery.com/honeydb/#about). 

The idea of my tool is to make it easier for the pentester/researcher/InfoSec pro to access this information and do something meaningful with it. To that end i have included in script WHOIS lookup and the ability to invoke an Nmap scan on a provided host.

## Active Development

The previous version of Mimir used the Mechanize lib to retrieve the Threat Feed and Bad Host list. Unfortunately there were some issues with the SSL implementation of Python2.7 with regards to mechanize. Therefore i have opted to use PyCurl instead.

Different versions of PyCurl work best with different versions of SSL. For this program to work properly PyCurl has to support OpenSSL. To that end i have added a shell script that automatically rebuilds PyCurl to work with OpenSSL and put further updates via `apt-get update` on hold if desired.

### Dependencies

```
pycurl
selenium 
blessings
ipwhois
pprint
```
### Known Issue

The project is in active development and as of yet there is a bug in the formatting of the Threat Feed data.

If you're interested in contributing to the develpopment of this tool i would encourage you to submit [a pull request](https://github.com/NullArray/Mimir/pulls) or suggestion [by opening a ticket](https://github.com/NullArray/Mimir/issues).

Thanks.

