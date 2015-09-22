# Ghost in the Shellcode 2014: Radioactive

**Category:** Crypto
**Points:** 250
**Description:**

> Find the key. [File](https://2014.ghostintheshellcode.com/radioactive-684d33ba06af30b9ad1a79abb3c6cecec74db18e) running at radioactive.2014.ghostintheshellcode.com:4324.

## Write-up

Write-up by [Matir](https://systemoverlord.com/).

The headers of the provided `radioactive-684d33ba06af30b9ad1a79abb3c6cecec74db18e` file contain `7zXZ`, indicating it’s `xz`-compressed data.

So, extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < radioactive-684d33ba06af30b9ad1a79abb3c6cecec74db18e > radioactive.txt`
* `unxz < radioactive-684d33ba06af30b9ad1a79abb3c6cecec74db18e > radioactive.txt`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x radioactive-684d33ba06af30b9ad1a79abb3c6cecec74db18e
```

Then, you can see that the included code is a Python script, the core of which is below:

```python
class RadioactiveHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    key = open("secret", "rb").read()
    cipher = AES.new(key, AES.MODE_ECB)

    self.request.send("Waiting for command:\n")
    tag, command = self.request.recv(1024).strip().split(':')
    command = binascii.a2b_base64(command)
    pad = "\x00" * (16 - (len(command) % 16))
    command += pad

    blocks = [command[x:x+16] for x in xrange(0, len(command), 16)]
    cts = [str_to_bytes(cipher.encrypt(block)) for block in blocks]
    for block in cts:
      print ''.join(chr(x) for x in block).encode('hex')

    command = command[:-len(pad)]

    t = reduce(lambda x, y: [xx^yy for xx, yy in zip(x, y)], cts)
    t = ''.join([chr(x) for x in t]).encode('hex')

    match = True
    print tag, t
    for i, j in zip(tag, t):
      if i != j:
        match = False

    del key
    del cipher

    if not match:
      self.request.send("Checks failed!\n")
    eval(compile(command, "script", "exec"))

    return
```

So, it looks for a `tag:command` pair, where the tag is hex-encoded and the command is base64-encoded. The command must be valid Python, passed through `compile` and `eval`, so you’ll need to send a response back to yourself via `self.request.send()`.

So how’s the tag calculated? Every 16-byte block of the command is encrypted in AES-ECB mode (so, two identical plaintexts == two identical ciphertexts) and then the encrypted blocks are XORed together, producing the final tag. My first thought was to generate a plaintext such that `len(plain) % 16 == 0`, then repeat it twice, so the XORs will cancel out and give a tag of `00…00`. Unfortunately, the padding must be at least one byte long, and the plaintext cannot contain null bytes.

So, we were also provided some sample code. One such example, decoded from its base64 representation, turns out to be:

```python
import os

self.request.send("Send command to eval: \n")
cmd = self.request.recv(1024).strip()

good = True
for b in cmd:
  if b not in '0123456789+-=/%^* ()':
    good = False

if good:
  self.request.send(str(eval(cmd)) + "\n")
else:
  self.request.send("???\n")
```

It turns out the line `good = False` (and two trailing newlines) are their own 16-byte block. We can append `good = True \n\n` to reset it to the value of `True`, and append it a second time to get our tag to come out correctly. Then we can simply provide `self.request.send(open('key').read())` when we receive our “Send command to `eval`:” prompt, and this got our flag.

Alternatively, because of a bug in the signature checking, we can just send the base64-encoded payload as long as we provide an empty tag:

```bash
$ base64 <<< "self.request.send(open('key').read())"
c2VsZi5yZXF1ZXN0LnNlbmQob3Blbigna2V5JykucmVhZCgpKQo=

$ echo ':c2VsZi5yZXF1ZXN0LnNlbmQob3Blbigna2V5JykucmVhZCgpKQo=' | nc -v radioactive.2014.ghostintheshellcode.com 4324
found 0 associations
found 1 connections:
     1: flags=82<CONNECTED,PREFERRED>
    outif en0
    src 192.168.107.131 port 59275
    dst 107.20.236.180 port 4324
    rank info not available
    TCP aux info available

Connection to radioactive.2014.ghostintheshellcode.com port 4324 [tcp/*] succeeded!
Waiting for command:
Welcom3ToTheNewAgeItsARevolutionISuppose
```

The flag is `Welcom3ToTheNewAgeItsARevolutionISuppose`.

## Other write-ups and resources

* <https://systemoverlord.com/blog/2014/01/19/ghost-in-the-shellcode-2014-radioactive/>
* <http://tasteless.eu/2014/01/gits-2014-radioactive-crypto-250/>
