#!/usr/bin/python
 
import smtplib
import mimetypes
import email
import email.mime.application
import sys
import os
import time
import datetime
from time import gmtime, strftime

now = strftime("%Y-%m-%d_%H.%M.%S", gmtime())

GMAILUSER = 'rasteberryan.pits@gmail.com'
GMAILPWD = 'Jiswwp!.@2802'
EMAILSENDER = 'rasteberryan.pits@gmail.com'
EMAILRECIPIENT = sys.argv[1]

# Root Directory
root_dir = "/home/pi/flask/donationbox-server/sites/compare/"

# Remove old diff files
cmd = "rm -f " + root_dir + "diff.jpg " + root_dir + "result.pdf"
os.system(cmd)

# Erstellung des 'diff' Bildes
cmd = "convert " + root_dir + "before.jpg " + root_dir + "after.jpg -compose difference -composite -evaluate Pow 2 -evaluate divide 3 -separate -evaluate-sequence Add -evaluate Pow 0.5 " + root_dir + "diff.jpg"
os.system(cmd)

# Erstellung der PDF Datei
time.sleep(3)
os.system("convert " + root_dir + "*.jpg " + root_dir + "result.pdf")
time.sleep(3)
 
# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'raspberry webshot'
msg['From'] = EMAILSENDER
msg['To'] = EMAILRECIPIENT
 
# The main body is just another attachment
body = email.mime.Text.MIMEText("""Hi, hier ein neues DIFF PDF!""")
msg.attach(body)
 
# PDF attachment block code
 
directory = root_dir + 'result.pdf'
 
# Split de directory into fields separated by / to substract filename
 
spl_dir=directory.split('/')
 
# We attach the name of the file to filename by taking the last
# position of the fragmented string, which is, indeed, the name
# of the file we've selected
 
filename=spl_dir[len(spl_dir)-1]
 
# We'll do the same but this time to extract the file format (pdf, epub, docx...)
 
spl_type=directory.split('.')
 
type=spl_type[len(spl_type)-1]
 
fp=open(directory,'rb')
att = email.mime.application.MIMEApplication(fp.read(),_subtype=type)
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)
 
# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate.
s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login(GMAILUSER,GMAILPWD)
s.sendmail(EMAILSENDER,[EMAILRECIPIENT], msg.as_string())
s.quit()
