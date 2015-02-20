#!/usr/bin/env python3


'''Send your ip adress by gmail if it changes'''

import sys
import platform
import os
import urllib.request
import time
import smtplib
import bz2
from email.mime.text import MIMEText


varargin = sys.argv
website = "http://23.95.33.126"
port = "80"
#website = "http://192.3.54.48"
#port = "18888"
#website = "http://echoip.com"
#port = "80"


def main():
    if len(varargin)==1: # If no arg, try to load the credentials from file
        cred = loadCred()
    elif len(varargin)==3: # If supplied with gmail and password, save the credential to a file
        if isinstance(varargin[1],str) and isinstance(varargin[2],str):
            cred = [str(varargin[1]),str(varargin[2])]
            CreateCred(cred)
        else:
            print('usage : python3 mailip.py [gmail password]')
            sys.exit()
    else:
        print('usage : python3 mailip.py [gmail password]')
        sys.exit()

    print('Started')
    print(__file__)
    if (platform.system()=='Linux'):
        print('Linux')
    if (platform.system()=='Windows'):
        print('Windows')

    try:
        configpath = os.path.expanduser("~/.config/mailip")
        os.chdir(configpath)
    except OSError:
        os.makedirs(configpath)
        os.chdir(configpath)

# Reading of the file containing last known ip adress
# If file is inexistant, create it
    try:
        file = open("ip.txt", "r")
    except IOError:
        print('Creating File')
        file = open("ip.txt", "w+")
    last_ip = file.read()
    file.close()

# Get ip adress from web server (mine or ipecho.net defined in global var).
    nbtries =5;
    success=0;
    tries=0;
    while(tries<nbtries and success==0) :
        try :
            print(website + ":" + port)
            s = urllib.request.urlopen(website + ':' + port ,timeout=10)
            success=1
        except :
            tries +=1
            print(tries)
    if tries>=nbtries :
        sys.exit('failed to connect to server')

    else :
         ip = s.read()
         ip = ip.decode()
         if (len(ip)<8 or len(ip)>15):#Check if site returned ip
            sys.exit('site did not return ip')

         if last_ip!=ip :
         # If ip changed since lastknown Ip,
         # send mail containing new ip adress with previously read crendetials
            mail(cred[0], 'ip change', ip ,cred[0], cred[1])
            file = open("ip.txt", "w+")
            file.write(ip)
            file.close()
            print('Sent')
         else:
             print('Same IP')



def mail(to, subject, text, gmail_user, gmail_pwd):
    msg = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject.encode('utf-8')
    msg.set_charset('utf-8')

    try:
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmail_user, gmail_pwd)
        mailServer.sendmail(gmail_user, to, text)
        mailServer.close()
    except:
        print('Error sending e-mail')
        raise

def loadCred():
    # Try to read the mailipCred file to extract the crypted user:password
    # string and return user and password in plain.
    try:
        os.chdir(os.path.expanduser("~/.config/mailip"))
        w = open('mailipCred','rb')
    except:
        print('Failed to read password')
        raise
    encrypt = bz2.decompress(w.read())
    w.close()
    # Decrypt the encrypted string and split by :
    en = encrypt.decode().split(':')
    gmail_user = en[0]
    gmail_pwd = en[1]
    return [gmail_user, gmail_pwd]


def CreateCred(cred):
    # Create and encrypt the string user:password with bz2 encode
    user = bz2.compress((cred[0] + ':' + cred[1]).encode())
    # Save the string to the mailipCred file
    os.chdir(os.path.expanduser("~/.config/mailip"))
    with  open('mailipCred','wb') as w:
        w.write(user)
        w.close()


if __name__ == '__main__':
  main()
