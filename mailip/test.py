#!/usr/bin/env python3
import argparse


parser = argparse.ArgumentParser(description='Mailip is used to send yourself an e-mail to your gmail account containing the ip adress of the machine if it has changed. On the first use you need to provide your Gmail credentials by adding the --cred argument')
parser.add_argument('--cred', nargs=2,metavar=('Gmail_address', 'Gmail_password'), help = "your Gmail credential for the first use.")

args = parser.parse_args()
print(args.cred)
