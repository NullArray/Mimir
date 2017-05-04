# Mimir
OSINT Threat Intel Interface - Named after the old Norse God of knowledge.

Mimir functions as a CLI to [HoneyDB](https://riskdiscovery.com/honeydb/about) which in short is an OSINT aggragative threat intel pool. Starting the program brings you to a menu the options for which are as follows.

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

And the Mozilla [Geckodriver](https://github.com/mozilla/geckodriver/releases)

## Note
This is a BETA release. Please report any bugs [by opening a ticket](https://github.com/NullArray/Mimir/issues).

Also, i am employing the PyCurl lib to retrieve the relevant data from HoneyDB, some versions of PyCurl work better with some versions of SSl than others. Should you find your version of PyCurl does not work with OpenSSL, please feel free to use the shellscript i have included in the repo to automatically rebuild PyCurl from source with OpenSSL support.

Thanks.

