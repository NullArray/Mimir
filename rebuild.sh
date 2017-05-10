#!/bin/bash

# rebuilds PyCurl to work with OpenSSL

# we will add some colored headers that make it easier to find obstacles 
# in the terminal output (which will be > 1000 lines...)
ESC="\x1b["
RESET=$ESC"39;49;00m"
RED=$ESC"31;01m"
GREEN=$ESC"32;01m"
YELLOW=$ESC"33;01m"
BLUE=$ESC"34;01m"

header() {
    echo -e "\n$YELLOW --- $1 --- $RESET\n"
}

echo -e "\n\n$GREEN"
echo -e "\
Build pycurl with openssl support\n\n\
Section numbers refer to\n\
https://gist.github.com/aerickson/f15133a7e56b2d7f27e3
"
echo -e "$RESET\n"



# remove eventually existing pycurl
header "0. remove python-pycurl"
sudo apt-get remove python-pycurl --yes

header "1. install build essentials"
sudo apt-get install build-essential fakeroot dpkg-dev --yes

header "2./3. make build dir"
mkdir ~/python-pycurl-openssl
cd ~/python-pycurl-openssl

if [ ! "$HOME/python-pycurl-openssl" = `pwd` ]; then
    echo -e "\n${RED}Cannot change to working dir. WTF?${RESET}\n"
    exit 1
fi

header "4. get pycurl sources"
sudo apt-get source python-pycurl --yes

header "5. get build dependencies for python-pycurl"
sudo apt-get build-dep python-pycurl --yes

header "6. install libcurl with openssl"
sudo apt-get install libcurl4-openssl-dev --yes

DIR=`find * -name 'pycurl*' -type d -print`
DSC=`find * -name '*.dsc' -type f -print`

echo
echo "DIR = $DIR"
echo "DSC = $DSC"
echo

header "7. unpack source archive"
sudo dpkg-source -x $DSC

header "8. change to package dir"
cd $DIR

header "9. edit debian/control file"
sudo cp debian/control ./control.gnutls
sudo cat ./control.gnutls | sed -e 's|libcurl4-gnutls-dev|libcurl4-openssl-dev|' | sudo tee ./control.openssl >/dev/null
sudo cp ./control.openssl debian/control

header "10. build package"
echo "hold on..."
echo "(crashdump of nosetests is 'normal')"
sudo PYCURL_SSL_LIBRARY=openssl dpkg-buildpackage -rfakeroot -b 2>&1 | sudo tee ../buildlog.txt >/dev/null
echo
echo -e $BLUE
sudo head ../buildlog.txt
echo -e $RESET
echo "   [ ... 1000+ more messages omitted ... ]"
echo -e $BLUE
sudo tail ../buildlog.txt
echo -e $RESET
echo
echo "find more output in ~/python-pycurl-openssl/buildlog.txt:"
wc -l  ../buildlog.txt

header "11. install via package manager"
sudo dpkg -i ../python-pycurl_*.deb

echo
echo "some other packages are available also now:"
ls ../*.deb
echo "they can be installed by 'sudo dpkg -i ../py...' from here."

echo
echo
echo "Disable apt-get update for PyCurl from now on?"
read -p 'Continue? Y/n : ' choice
if [[ $choice == 'y' ]]; then
	sudo apt-mark hold python-pycurl
	echo "PyCurl updates put on hold"
else
	echo "PyCurl updates remain enabled"
fi
