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
import argparse


parser = argparse.ArgumentParser(description='Mailip is used to send yourself an e-mail to your gmail account containing the ip adress of the machine if it has changed. On the first use you need to provide your Gmail credentials by adding the --cred argument')
parser.add_argument('--cred', nargs=2,metavar=('G_address', 'G_password'), help = "your Gmail credentials for the first use.")

args = parser.parse_args()
website = ("http://23.95.33.126/ip/","http://echoip.com"
            ,"wtfismyip.com/text")
port = ("80","80","80")
def main():
    if not args.cred: # If no arg, try to load the credentials from file
        cred = loadCred()
    else: # If supplied with gmail and password, save the credential to a file
            cred = args.cred
            CreateCred(cred)

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
    nbtries = len(website)
    success=0
    tries=0
    while(tries<nbtries and success==0) :
        try :
            print(website[tries])
            s = urllib.request.urlopen(website[tries] ,timeout=3)
            success=1
        except :
            tries +=1
            print(tries)
    if tries>=nbtries :
        sys.exit('failed to connect to servers')

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
