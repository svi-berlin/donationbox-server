#!/usr/bin/python

import os
import sys 

domain = str(sys.argv[1])
name = str(sys.argv[2])
image = "/home/pi/flask/donationbox-server/sites/compare/" + str(name) + ".jpg"

cmd = "rm -f " + image
os.system(cmd)

cmd = "xvfb-run --server-args='-screen 0, 640x960x24' cutycapt --url=" + str(domain) + " --out=" + image
#print cmd
os.system(cmd)




