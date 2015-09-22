# ASIS Cyber Security Contest Finals 2014: A familiar system

**Category:** Crypto
**Points:** 200
**Description:**

> The flag is encrypted by this [code](crsh_716c88fb8dcc3914b5b5711afecb318e), can you decrypt it after finding the system?

## Write-up

Write-up by [Hacknamstyle](http://hacknamstyle.net). Let’s see what [the provided file](crsh_716c88fb8dcc3914b5b5711afecb318e) could be:

```bash
$ file crsh_716c88fb8dcc3914b5b5711afecb318e
crsh_716c88fb8dcc3914b5b5711afecb318e: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < crsh_716c88fb8dcc3914b5b5711afecb318e > crsh`
* `unxz < crsh_716c88fb8dcc3914b5b5711afecb318e > crsh`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x crsh_716c88fb8dcc3914b5b5711afecb318e
```

Let’s find out what the extracted file is:

```bash
$ file crsh
crsh: POSIX tar archive
```

Let’s extract it:

```bash
$ tar xvf crsh
x crsh/: Refusing to overwrite archive
x crsh/crsh.py
x crsh/flag.enc
tar: Error exit delayed from previous errors.
```

## The Challenge

The file `crsh.py` contains the two functions `makey` and `encrypt`. From this we can already deduce that we will need to use this information to decrypt the file `flag.enc`. First we need to determine the type of encryption used. We make two observations:

1. A random value `q` is chosen, and all operations are performed modulo `q`.
2. In the key generation algorithm, some value `z` is chosen, and then `h = g1**z` is calculated. Variable `z` goes in the private key, while the result `h` goes in the public key.

With this in mind I finally ended up with [ElGamal encryption](https://en.wikipedia.org/wiki/ElGamal_encryption). Once this is known we can look up the decryption algorithm for ElGamal, and apply it to the variables in our challenge:

```python
def decrypt(ciphertext, privkey, pubkey):
    # Unpack key and ciphertext
    x1, x2, y1, y2, z = privkey
    q, g1, g2, c, d, h = pubkey
    u1, u2, e, v = ciphertext

    # Alice calculates s = c_1^x
    s = pow(u1, z, q)
    # and then computes m = c_2 * s^-1
    m = divmod(e * invert(s, q), q)[1]
    return hex(m)[2:].decode("hex")
```

The comments refer to the constants being used on [Wikipedia](https://en.wikipedia.org/wiki/ElGamal_encryption). This is sufficient to decrypt a message **if we know the private key**. For completeness, the challenge actually contains a [Cramer–Shoup cryptosystem](https://en.wikipedia.org/wiki/Cramer%E2%80%93Shoup_cryptosystem). This can be considered an extension of the ElGamal system (but we don't need to be this precise in order to solve the challenge).

All that remains is finding the private key. Let's take a look at the key generation algorithm:

```python
def makey():
	q = next_prime(randint(1, 2**1024))

	x1 = next_prime(randint(1, q-1))
	x2 = next_prime(x1)

	y1 = next_prime(x2)
	y2 = next_prime(y1)

	z = next_prime(y2)

	g1 = next_prime(z)
	g2 = next_prime(g1)

	c = divmod(pow(g1, x1, q)*pow(g2, x2, q), q)[1]
	d = divmod(pow(g1, y1, q)*pow(g2, y2, q), q)[1]
	h = pow(g1, z, q)

	pubkey = (q, g1, g2, c, d, h)
	privkey = (x1, x2, y1, y2, z)
	return (pubkey, privkey)
``` 

We see that it uses `next_prime`, which is a function that can be efficiently inverted. That is, we can create the function `prev_prime`. Now remark that the public key contains the constants `g1` and `g2`. We can calculate `z = prev_prime(g)`. Similarly we can use `prev_prime` to find the values for `y2`, `y1`, `x2`, and `x1`. Hence we can derive the private key from the public key! The solution becomes:

```python
from gmpy import *

def decrypt(ciphertext, privkey, pubkey):
    """"ElGamal Decryption"""
    # Unpack key and ciphertext
    x1, x2, y1, y2, z = privkey
    q, g1, g2, c, d, h = pubkey
    u1, u2, e, v = ciphertext

    # Alice calculates s = c_1^x
    s = pow(u1, z, q)
    # and then computes m = c_2 * s^-1
    m = divmod(e * invert(s, q), q)[1]
    return hex(m)[2:].decode("hex")

def prev_prime(num):
    """"Get the larger prime smaller than num"""
    num -= 1
    while not is_prime(num):
        num -= 1
    return num

def pubkey2privkey(pubkey):
    """"Convert public key to private key using prev_prime"""
    # Unpack pubkey
    q, g1, g2, c, d, h = pubkey
    # Derive private key
    z = prev_prime(g1)  # g1 = next_prime(z)
    y2 = prev_prime(z)  # z = next_prime(y2)
    y1 = prev_prime(y2) # y2 = next_prime(y1)
    x2 = prev_prime(y1) # y1 = next_prime(x2)
    x1 = prev_prime(x2) # x2 = next_prime(x1)
    return (x1, x2, y1, y2, z)

# Apply attack to data in flag.enc
target_pubkey = (mpz(136251271151175798114432982938026229490172110401533005102755262286989049184622583417708312009201423476024122677912469680055108982880741528463299142672020834652185527641834721206398483386320729427665613285937265257500825945169037119499345376317962489316486718729170177878788547880596679146803674652102959291179L), mpz(71445390607919938548377475361074566973666877698962004381686815881759650363064790907205389724727052137547259275540047248324480810969042982358139755944485006293081693292128510719329497724780095449564775706193685016091515868306878669276650004788889866268563082218902602391430478108176895385536441463628368479691L), mpz(71445390607919938548377475361074566973666877698962004381686815881759650363064790907205389724727052137547259275540047248324480810969042982358139755944485006293081693292128510719329497724780095449564775706193685016091515868306878669276650004788889866268563082218902602391430478108176895385536441463628368480207L), mpz(108199964103615859008641230860441564013546022099141268729672372560684354711029024967645311655477601297528967214190176938354612973975648677808462780788853857235728443378937276686560734685975860104201150877752699741509893128491453639598002202233433849963771486923929948182126953422409316505411725704660574071657L), mpz(103402410846165640937714634826853699897953021060814854902226893930824546559478506490958509691172995834949498468163369749905491304339347496145685254419406709457509584848035666518698160042608561655338153398962281529505944744194818819405360595447357300235672126457982381082804720943718414140633702130115821518928L), mpz(116340711871909700306245119761735910172833445394742389374011288239236399789939214131715064909418737704146479936263956091201586261917588169097003026421666887999597157485524925727710226313542982324774527228728935095548200397393540416160234666725112551485046369907177780830026445351468830181648589841619040173447L))
target_c = (mpz(95467029105787819790685969501366652001448206091850219200437950980373198908537653149971642327326341562268633482168133967260392708002179128551446621791484500920123876866983047200450805908685344827646021342534877486305386714673539389693570659549538563696044252832011728553065377412813197782577269476428499901380L), mpz(89595710576920408480354520361707208226997008947621263700559849048228174093448090149075663223527046593283363587635794437708287463841014370347924449040164626126884978025404190308594954049190456014671432009757978067180946291164237407302064238478012485599209052294009083110639149028553486139617037940588192592074L), mpz(57101456812661040956911779152454680172788225654576055105325326802166273530593058160592967123782888106635604456486570389449265108078292983788415457231056869140594423238818468521681863517528522462778250100010993034244098761920700791617733626499616701097597271369053126885898596529980095548583743153472666478505L), mpz(130115388527739990394206680758957845883765682145236104898391558273731695522796485926165074063891018632144470079672768643505790273888231579876368492622104212560577966249611966815224426991815509628590538262064965030005368864440395952711567523963516639208866726152754741399145669201328995650062154785975721499147L))

target_privkey = pubkey2privkey(target_pubkey)
print decrypt(target_c, target_privkey, target_pubkey)

# Result: ASIS_e4e6417b4baebb748da67e33f6e091d5
```

Hence the flag is `ASIS_e4e6417b4baebb748da67e33f6e091d5`.

## Other write-ups and resources

* Write-up by [tasteless](http://tasteless.eu/2014/10/asis-ctf-finals-2014-a-familiar-system/)
* <https://beagleharrier.wordpress.com/2014/10/13/asis-ctf-finals-2014a-familiar-system-writeup/>
