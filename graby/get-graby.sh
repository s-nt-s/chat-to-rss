#!/bin/bash
LAST=$(curl -sS "https://php-download.com/package/j0k3r/graby" | grep "selected=\"selected\"" | cut -d'"' -f2)
URL="https://php-download.com/downloads/j0k3r/graby/${LAST}/j0k3r_graby_${LAST}_require.zip"
wget -O graby.zip "$URL"
unzip -o -q graby.zip 'vendor/*'
rm graby.zip

