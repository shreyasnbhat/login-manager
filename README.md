# login-manager
A simple login manger to manage user accounts for Cyberroam login.

All credentials are stored locally in a file `credentials.json`. 

### Script Options in `login.py`
- Add new user credentials
- Remove user credentials
- Brute force password for a user
- Show all user credentials
- Check if accounts use standard passwords

### Timeout Mechanism in `connect.py`
In order to avoid unnecessary network requests to check Internet connection, a variable timeout is being used.
If connected to the network the timeout is set to `5 seconds` initially. The timeout increases by `5 seconds` after every successful internet check. After the timeout reaches `30 seconds` it stays constant.

### v1
- Allows login via multiple users.
- Allows automatic switch to another user id if current id has exhausted data limit.

### v2
- Monitors network and triggers login functionality when not connected to internet.
- Internet detection is handled via polling with a variable timeout.

### v3 (ToDo)
- From a set of credentials a list of users can be assigned as `active` which implies that only those users internet id's will be used. This is stored in a file `users.txt`
