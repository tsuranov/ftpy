#!/usr/bin/env python3
import ftplib
import os
 

print ("Start FTP downloader!")

ftp = ftplib.FTP('ftp.debian.org')
ftp.login() 

ftp.retrlines('LIST')

#ftp.cwd('debian')
filenames = ftp.nlst()

print ("End FTP downloader!")