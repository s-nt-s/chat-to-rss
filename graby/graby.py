#!/usr/bin/python3
import json
import sys
from subprocess import check_output, STDOUT
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

url = sys.argv[1]
js = check_output(['./graby.php', url], stderr=STDOUT).decode('UTF-8')
js = json.loads(js)
js = json.dumps(js, indent=4, sort_keys=True)
print(js)
