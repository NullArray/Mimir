# Mimir
OSINT Threat Intel Interface - Named after the old Norse God of knowledge.

Mimir functions as a CLI to [HoneyDB](https://riskdiscovery.com/honeydb/about) which in short is an OSINT aggregative threat intel pool. Starting the program brings you to a menu the options for which are as follows.

```
1. Fetch Threat Feed        5. Visualize Top Malicious Hosts in Browser
2. Fetch Bad Host List      6. Visualize Top Targeted Services in Browser
3. Perform WHOIS Lookup     7. Visualize Results for Single Host in Browser
4. Invoke Nmap Scan         8. Quit
```
The purpose of this tool is to make intelligence gathering easier by including functionality to save the Threat Feed and Bad Host lists, and invoke either an in-script WHOIS lookup or Nmap scan to learn more about the target hosts. Logs are saved in the current working directory for future reference and further processing.

HoneyDB provides a data visualization service, this can be accessed via Mimir by selecting their respective options. Selenium will 
then employ the Geckodriver to open the pages.

## Dependencies

```
pycurl
selenium 
blessings
ipwhois
pprint
```

[Nmap](https://nmap.org/) and the Mozilla [Geckodriver](https://github.com/mozilla/geckodriver/releases)

To install the Python2.7 modules Mimir depends on please feel free to use the requirements file i have made for this project like so.

`pip install -r requirements.txt`

## Update

Some versions of PyCurl work better with some versions of SSL than others. This is important because HoneyDB makes use of OpenSSL and having a version that does not support it makes Mimir incompatible with HoneyDB. To that end I have added some logic that lets Mimir detect your version of PyCurl and automatically rebuild it from source to a version that does support OpenSSL. It does so by invoking the `rebuild.sh` shell script that is included in this repo.

