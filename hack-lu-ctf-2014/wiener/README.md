# Hack.lu CTF 2014: Wiener

**Category:** Crypto
**Points:** 300
**Author:** javex
**Description:**

> It’s gold rush time! The New York Herald just reported about the Californian gold rush. We know a sheriff there is hiring guys to help him fill his own pockets. We know he already has a deadful amount of gold in his secret vault. However, it is protected by a secret only he knows. When new deputies apply for the job, they get their own secret, but that only provides entry to a vault of all deputy sheriffs. No idiot would store their stuff in this vault. But maybe we can find a way to gain access to the sheriff’s vault? Have a go at it: `nc wildwildweb.fluxfingers.net 1426`
>
> You might also need [this](wiener_38ff175d336b9c75fbf1b77290978015.py).

## Write-up

The challenge name gives a hint about Wiener, and the Python code shows that RSA is involved (see `asn1_encode_priv_key`). After reading the [Wiener attack details](http://en.wikipedia.org/wiki/Wiener%27s_attack), we are able to retrieve the private exponent `d` from the pair `(e, n)` if `d` is small enough. The challenge code (around line 220) gives us:

```python
d = prng.getrandbits(2048 // 5)
```

We can extract the pair `(e, n)` through the `p` command:

```bash
$ nc wildwildweb.fluxfingers.net 1426
Well if it isn't another one of those shave tails again. Don't you dare think this is gonna be an easy job here, we take no coffee boilers just so ya' know. If you're sure you want to join our deputy ranks, just apply here. If you got any problems just lemme know by typing 'h'.
Command: h
These are the questions you can ask me:
h: Ask the sheriff for help. He might not react too friendly...
r: Get a lock and a locker code. This way you can also unlock the shared locker for everyone!
l: Get a list of all guys that have locks.
p: Get the lock for a particular guy. Why would you need that?
Command: p
So whose lock do you wanna see? sheriff
Here this is sheriff's lock. Why do you need it, hmm?
ssh-rsa AAAAB3NzaC1yc2EAAAEAAoX41P4pzhFgXt8iGGiTfBtwrjduNNZ/m7eMKaLXnKRqYOoCpw/bQOgFtdhUJVlosrHwQ5Y9zWFxTOT8XHDsxNdWrRaF1mHbOdFagB0cOC7ZegSPD4XZCcgRaR0//iYutwzNH6fboap5E58hwUs9/pU0BJHP86WmrpYEMpV4259bzBkuFqpi9oeoA45gwBUY+MyqC+/ladra6OSTEKejw73c9jf8guU0C+9BBbUztqUxiVZQsu+jN9lMenZEd2e1EpoEvPPNlbtg9r/RoSZYUwEkrYxv1xZSuODrSC/MR1BDtBDfxP5fvGvaCMphJEKEpKtbMRvGad8MdTUmp5waVwAAAQACrrY39hUq/U+zot0WWuydW0XnDSuC54o1P3oXUYWdGW9Wy20RcAGV8Qaac9nlcQlQuBQimrTFVJODwsh+DNl/kEdIoTAkANx2tCWR2hfauvlGqq8WQPEyevFr5FuIMGA5R6nDMJyk1syfGivP2s8oX7wvcw5RWuHZNZHM2Y9cRnTsSlhZJkcA9wCk9Nz3w8NbvFefbr+A2jPGwR9oZVCSu+Zw1SJbjlcdWW/kJttZpqBar3ezkXRIss+8s71ke0Z3KxMTP8aP+ryzdSNyuUmjcEuFlt9KRPCFOT7iv4D485NxntlKs0iFL2peDEk++jLaW/YBBjoDO+r3O6R9ggXb sheriff
```

The format of the base64 blob is a set of `(len[4], item[len])` for the identifier string, `e` and `n`:

* `"00 00 00 07"`: `"ssh-rsa"`
* `"00 00 01 00"`: public exponent
* `"00 00 01 00"`: modulus

We then recover `d` and the `phi` [totient](http://en.wikipedia.org/wiki/Euler%27s_totient_function) thanks to the Wiener attack, calculate `p` (or `q`) and reuse the `asn1_encode_priv_key` Python function from the original challenge to generate the private key.

The [attack is implemented in Python](https://github.com/pablocelayes/rsa-wiener-attack) (you need to clone the Git repo of the attack to get the correct `import) and we eventually end up with the following code:

```python
import ContinuedFractions, Arithmetic, RSAvulnerableKeyGenerator
import sys
import base64
import struct
import math
import fractions
import gmpy
import sympy

import pyasn1_modules.rfc3447
import pyasn1.codec.ber.encoder

def hack_RSA(e,n):
  '''
  Finds d knowing (e,n)
  applying the Wiener continued fraction attack
  '''
  frac = ContinuedFractions.rational_to_contfrac(e, n)
  convergents = ContinuedFractions.convergents_from_contfrac(frac)

  for (k,d) in convergents:

    #check if d is actually the key
    if k!=0 and (e*d-1)%k == 0:
      phi = (e*d+1)//k
      s = n - phi + 1
      # check if the equation x^2 - s*x + n = 0
      # has integer roots
      discr = s*s - 4*n
      if(discr>=0):
        t = Arithmetic.is_perfect_square(discr)
        if t!=-1 and (s+t)%2==0:
          print("Hacked!")
          return d,phi

def test_hack_RSA(e,n):
  print("Testing Wiener Attack")
  times = 1

  while(times>0):
    #e,n,d = RSAvulnerableKeyGenerator.generateKeys(1024)
    print("(e,n) is (", e, ", ", n, ")")

    hacked_d = hack_RSA(e, n)

    print("hacked_d = ", hacked_d)
    print("-------------------------")
    times -= 1

  return hacked_d

def asn1_encode_priv_key(N, e, d, p, q):
  key = pyasn1_modules.rfc3447.RSAPrivateKey()
  dp = d % (p - 1)
  dq = d % (q - 1)
  qInv = gmpy.invert(q, p)
  #assert (qInv * q) % p == 1
  key.setComponentByName('version', 0)
  key.setComponentByName('modulus', N)
  key.setComponentByName('publicExponent', e)
  key.setComponentByName('privateExponent', d)
  key.setComponentByName('prime1', p)
  key.setComponentByName('prime2', q)
  key.setComponentByName('exponent1', dp)
  key.setComponentByName('exponent2', dq)
  key.setComponentByName('coefficient', qInv)
  ber_key = pyasn1.codec.ber.encoder.encode(key)
  pem_key = base64.b64encode(ber_key).decode("ascii")
  out = ['-----BEGIN RSA PRIVATE KEY-----']
  out += [pem_key[i:i + 64] for i in range(0, len(pem_key), 64)]
  out.append('-----END RSA PRIVATE KEY-----\n')
  out = "\n".join(out)
  return out.encode("ascii")

if __name__ == "__main__":
  sys.setrecursionlimit(1500)

  keydata = base64.b64decode(sys.argv[1])

  parts = []
  while keydata:
    # read the length of the data
    dlen = struct.unpack('>I', keydata[:4])[0]

    # read in <length> bytes
    data, keydata = keydata[4:dlen+4], keydata[4+dlen:]

    parts.append(data)

  e_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in
      parts[1]]))
  n_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in
      parts[2]]))

  print hex(e_val)

  d_val, phi_val = test_hack_RSA(e_val, n_val)
  #d_val = 724746542590011388513367385228693742222740657137483753552318433232068370338961145215199994578740789016238655979015224570943L
  #phi_val = 338630205260455689413627911306068443537112802550361922213620660503310212139001530156458392949653034244789612680980241965923780722889133495349537107789761426092510299239678696031652780059016898519278860185536978111680123402473365833456785718098200501968322228116681190425490850863660038143310790555506293106612832752816526294946244330554558811312381169746599669997187914877490856336218310169927726408740994026774015446804415510971495034414170679517574320170326096806247477803294330492724911633596245761058343100118785517282649648198386928412053124797987039344718844068821755346442016872442675863694586221009879142600L

  print("n:%s\n"% n_val)
  print("e:%s\n"% e_val)
  print("d:%s\n"% d_val)
  print("phi:%s\n"% phi_val)

  p_val = sympy.Symbol('p_val')
  eq = sympy.Eq(p_val*p_val + (n_val+1-phi_val)*p_val + n_val)
  solved = sympy.solve(eq, p_val)

  p_val = int(-1*(solved[0]))
  q_val = int(-1*(solved[1]))

  print n_val == p_val*q_val

  print("p:%s\n"% p_val)
  print("q:%s\n"% q_val)

  print repr(p_val)
  print type(p_val)
  print asn1_encode_priv_key(n_val, e_val, d_val, p_val, q_val)
```

Running the script reveals the private key:

```bash
$ python RSAwienerHacker.py 'AAAAB3NzaC1yc2EAAAEAAoX41P4pzhFgXt8iGGiTfBtwrjduNNZ/m7eMKaLXnKRqYOoCpw/bQOgFtdhUJVlosrHwQ5Y9zWFxTOT8XHDsxNdWrRaF1mHbOdFagB0cOC7ZegSPD4XZCcgRaR0//iYutwzNH6fboap5E58hwUs9/pU0BJHP86WmrpYEMpV4259bzBkuFqpi9oeoA45gwBUY+MyqC+/ladra6OSTEKejw73c9jf8guU0C+9BBbUztqUxiVZQsu+jN9lMenZEd2e1EpoEvPPNlbtg9r/RoSZYUwEkrYxv1xZSuODrSC/MR1BDtBDfxP5fvGvaCMphJEKEpKtbMRvGad8MdTUmp5waVwAAAQACrrY39hUq/U+zot0WWuydW0XnDSuC54o1P3oXUYWdGW9Wy20RcAGV8Qaac9nlcQlQuBQimrTFVJODwsh+DNl/kEdIoTAkANx2tCWR2hfauvlGqq8WQPEyevFr5FuIMGA5R6nDMJyk1syfGivP2s8oX7wvcw5RWuHZNZHM2Y9cRnTsSlhZJkcA9wCk9Nz3w8NbvFefbr+A2jPGwR9oZVCSu+Zw1SJbjlcdWW/kJttZpqBar3ezkXRIss+8s71ke0Z3KxMTP8aP+ryzdSNyuUmjcEuFlt9KRPCFOT7iv4D485NxntlKs0iFL2peDEk++jLaW/YBBjoDO+r3O6R9ggXb'
0x285f8d4fe29ce11605edf221868937c1b70ae376e34d67f9bb78c29a2d79ca46a60ea02a70fdb40e805b5d854255968b2b1f043963dcd61714ce4fc5c70ecc4d756ad1685d661db39d15a801d1c382ed97a048f0f85d909c811691d3ffe262eb70ccd1fa7dba1aa79139f21c14b3dfe95340491cff3a5a6ae9604329578db9f5bcc192e16aa62f687a8038e60c01518f8ccaa0befe569dadae8e49310a7a3c3bddcf637fc82e5340bef4105b533b6a531895650b2efa337d94c7a76447767b5129a04bcf3cd95bb60f6bfd1a12658530124ad8c6fd71652b8e0eb482fcc475043b410dfc4fe5fbc6bda08ca61244284a4ab5b311bc669df0c753526a79c1a57L
n:338630205260455689413627911306068443537112802550361922213620660503310212139001530156458392949653034244789612680980241965923780722889133495349537107789761426092510299239678696031652780059016898519278860185536978111680123402473365833456785718098200501968322228116681190425490850863660038143310790555506293106653050174262471649179173093656763946257235681980586392230447218179278964626176124426615857733950102117938674282636936094069075258237416065546593509302494726576026227551920883962084579635168761189995794814926094510046419165007371450799003658587100556051088147493947712592469412133312536422828670173807709914587

e:318540665379393469901456665807211509077755719995811520039095212139429238053864597311950397094944291616119321660193803737677538864969915331331528398734504661147661499115125056479426948683504604460936703005724827506058051215012025774714463561829608252938657297504427643593752676857551877096958959488289759878259498255905255543409142370769036479607835226542428818361327569095305960454592450213005148130508649794732855515489990191085723757628463901282599712670814223322126866814011761400443596552984309315434653984387419451894484613987942298157348306834118923950284809853541881602043240244910348705406353947587203832407

d:724746542590011388513367385228693742222740657137483753552318433232068370338961145215199994578740789016238655979015224570943

phi:338630205260455689413627911306068443537112802550361922213620660503310212139001530156458392949653034244789612680980241965923780722889133495349537107789761426092510299239678696031652780059016898519278860185536978111680123402473365833456785718098200501968322228116681190425490850863660038143310790555506293106612832752816526294946244330554558811312381169746599669997187914877490856336218310169927726408740994026774015446804415510971495034414170679517574320170326096806247477803294330492724911633596245761058343100118785517282649648198386928412053124797987039344718844068821755346442016872442675863694586221009879142600

True
p:28216117316929874067495888027767527011360661622486842768414059951572932145196930641365509243766454218518793508840136548374994021850853203018205749779390383366761851772055038753940967432004901699256177783249460134792699230632136386268348434203012426963129659057781488950062703849444443906614331812260961682887

q:12001304129015480165432875074437607933493850611499879464845243350215176144760883615322622081442653872645865326992384034722586201972392183010813439352778246403016897976571514715418700569567613729681273931557848857971070286176848136118602099586101089743239644367344468295964691411425416652519752140536869089101

28216117316929874067495888027767527011360661622486842768414059951572932145196930641365509243766454218518793508840136548374994021850853203018205749779390383366761851772055038753940967432004901699256177783249460134792699230632136386268348434203012426963129659057781488950062703849444443906614331812260961682887L
<type 'long'>
-----BEGIN RSA PRIVATE KEY-----
MIIENgIBAAKCAQACrrY39hUq/U+zot0WWuydW0XnDSuC54o1P3oXUYWdGW9Wy20R
cAGV8Qaac9nlcQlQuBQimrTFVJODwsh+DNl/kEdIoTAkANx2tCWR2hfauvlGqq8W
QPEyevFr5FuIMGA5R6nDMJyk1syfGivP2s8oX7wvcw5RWuHZNZHM2Y9cRnTsSlhZ
JkcA9wCk9Nz3w8NbvFefbr+A2jPGwR9oZVCSu+Zw1SJbjlcdWW/kJttZpqBar3ez
kXRIss+8s71ke0Z3KxMTP8aP+ryzdSNyuUmjcEuFlt9KRPCFOT7iv4D485NxntlK
s0iFL2peDEk++jLaW/YBBjoDO+r3O6R9ggXbAoIBAAKF+NT+Kc4RYF7fIhhok3wb
cK43bjTWf5u3jCmi15ykamDqAqcP20DoBbXYVCVZaLKx8EOWPc1hcUzk/Fxw7MTX
Vq0WhdZh2znRWoAdHDgu2XoEjw+F2QnIEWkdP/4mLrcMzR+n26GqeROfIcFLPf6V
NASRz/Olpq6WBDKVeNufW8wZLhaqYvaHqAOOYMAVGPjMqgvv5Wna2ujkkxCno8O9
3PY3/ILlNAvvQQW1M7alMYlWULLvozfZTHp2RHdntRKaBLzzzZW7YPa/0aEmWFMB
JK2Mb9cWUrjg60gvzEdQQ7QQ38T+X7xr2gjKYSRChKSrWzEbxmnfDHU1JqecGlcC
NAEYqi24CTaHQf3Lk2yCWcrgmbWRTbmjbuDDxDlbu2owScEHSrCAVSlpmNdxKd83
7DSKND8CgYAoLluTIZD4lI35NEhy7M1OrXHXJbgxB38vNr+qcSKiaDuP2gi7LM0I
LF3UlBhNNjKnSk79aFH3v3jjbRLnFaOiFCz+++M2J6MYnNGJrjYiYZvTFgGeL08F
qxwplI27UVPK5dxbompgejkQJK4l3JDHVauyPyCUwQai3Fqz4dWFxwKBgBEXJg1E
F7WqxYNkCjluOXUvFk9PT91+nnR+SCqCsufuSoo0MlTiWgJlHdcuOPB+wUoVa2Ch
8xRQZ++uPEVoYXxYXEZxbGV1lPJr70fVQ1/zp9Y5uQy5qAzlK7WHbVA49qCahhDq
QKiOfP4v9Sv1+/HBtWrFAVZx+3xyLhY0fO9NAjQBGKotuAk2h0H9y5NsglnK4Jm1
kU25o27gw8Q5W7tqMEnBB0qwgFUpaZjXcSnfN+w0ijQ/AjQBGKotuAk2h0H9y5Ns
glnK4Jm1kU25o27gw8Q5W7tqMEnBB0qwgFUpaZjXcSnfN+w0ijQ/AoGAGgXFN5+n
gMSvyOCCOSN2oM9h0YogHJqbn5/iOLHPZjrSPGITcgyJkrdfvmv9z96XGLpAsSu3
BBHNM4wsyKpJVGhYzJT0MaVT5+vWm/FWuIrl59A2fRVJUZP7ThbFN84UR3Aulv9x
q7YgGrkMcwMYDOYZxsIq59S/slZPkl59i30=
-----END RSA PRIVATE KEY-----
```

Let’s copy the private key to the file `private.key` and verify that the public key generated from the private key is the same:

```bash
$ ssh-keygen -y -f private.key
ssh-rsa AAAAB3NzaC1yc2EAAAEAAoX41P4pzhFgXt8iGGiTfBtwrjduNNZ/m7eMKaLXnKRqYOoCpw/bQOgFtdhUJVlosrHwQ5Y9zWFxTOT8XHDsxNdWrRaF1mHbOdFagB0cOC7ZegSPD4XZCcgRaR0//iYutwzNH6fboap5E58hwUs9/pU0BJHP86WmrpYEMpV4259bzBkuFqpi9oeoA45gwBUY+MyqC+/ladra6OSTEKejw73c9jf8guU0C+9BBbUztqUxiVZQsu+jN9lMenZEd2e1EpoEvPPNlbtg9r/RoSZYUwEkrYxv1xZSuODrSC/MR1BDtBDfxP5fvGvaCMphJEKEpKtbMRvGad8MdTUmp5waVwAAAQACrrY39hUq/U+zot0WWuydW0XnDSuC54o1P3oXUYWdGW9Wy20RcAGV8Qaac9nlcQlQuBQimrTFVJODwsh+DNl/kEdIoTAkANx2tCWR2hfauvlGqq8WQPEyevFr5FuIMGA5R6nDMJyk1syfGivP2s8oX7wvcw5RWuHZNZHM2Y9cRnTsSlhZJkcA9wCk9Nz3w8NbvFefbr+A2jPGwR9oZVCSu+Zw1SJbjlcdWW/kJttZpqBar3ezkXRIss+8s71ke0Z3KxMTP8aP+ryzdSNyuUmjcEuFlt9KRPCFOT7iv4D485NxntlKs0iFL2peDEk++jLaW/YBBjoDO+r3O6R9ggXb
```

Now let’s log in to the sheriff’s vault:

```bash
$ ssh -p 1427 -i private.key sheriff@wildwildweb.fluxfingers.net
Woah look how much gold that old croaker has: flag{TONS_OF_GOLD_SUCH_WOW_MUCH_GLOW}
Connection to wildwildweb.fluxfingers.net closed.
```

The flag is `flag{TONS_OF_GOLD_SUCH_WOW_MUCH_GLOW}`.

## Other write-ups and resources

* [Writeup by captchaflag](http://www.captchaflag.com/blog/2014/10/23/hack-dot-lu-2014-wiener/)
* <https://ctfcrew.org/writeup/87>
