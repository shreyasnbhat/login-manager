#!/usr/bin/python3

from urllib.request import urlopen, URLError
import time
from login import login, populate

timeout = 5
populate()


def read_active_users():
    global users
    # users.txt stores user id's of active internet id's
    with open('users.txt') as f:
        users = f.read().splitlines()


def connect():
    flag = False
    for i in users:
        response = login(i)
        if 'successfully' in response:
            print(response, "as", i)
            flag = True
            break

    if not flag:
        print("All internet id's have been exhausted.")
    else:
        print("Connection Established.")
        timeout = 120
        print("Timeout is set to", timeout)

    return flag


def poll():
    global timeout
    while(1):
        print("Checking Connection...")
        time.sleep(timeout)
        flag = False
        try:
            response = urlopen('http://4.2.2.2', timeout=10)
            if response.msg != 'Please login.':
                flag = True
                timeout = 120
                print("Timeout is set to", timeout)
            else:
                timeout = 5
        except URLError as er:
            print("Internet is not connected")
            timeout = 5
            print("Timeout is set to", timeout)

        if not flag:
            print("Connecting to Internet...")
            connected = connect()

            if not connected:
                break


if __name__ == '__main__':
    read_active_users()
    poll()
