# RuCTF 2014 Quals: Crypto 500 - [Related](https://github.com/HackerDom/ructf-2014-quals/tree/master/tasks/related)

> Two agents, Alex and Jane, have simultaneously known very secret message and transmitted it to Center. You know following:
> 1) They used RSA with [this public key](key.pub)
> 2) They sent exactly the same messages except the signatures (name appended, eg. "[message]Alex")
> 3) They did encryption this way:
>	c, = pubKey.encrypt(str\_to\_num(message), 1) # using RSA from Crypto.PublicKey
>	c = num\_to\_str(c).encode('hex')
> 4) And here are cryptograms you have intercepted:
>
> "61be5676e0f8311dce5d991e841d180c95b9fc15576f2ada0bc619cfb991cddfc51c4dcc5ecd150d7176c835449b5ad085abec38898be02d2749485b68378a8742544ebb8d6dc45b58fb9bac4950426e3383fa31a933718447decc5545a7105dcdd381e82db6acb72f4e335e244242a8e0fbbb940edde3b9e1c329880803931c"
>
> "9d3c9fad495938176c7c4546e9ec0d4277344ac118dc21ba4205a3451e1a7e36ad3f8c2a566b940275cb630c66d95b1f97614c3b55af8609495fc7b2d732fb58a0efdf0756dc917d5eeefc7ca5b4806158ab87f4f447139d1daf4845e18c8c7120392817314fec0f0c1f248eb31af153107bd9823797153e35cb7044b99f26b0"
>
> Now tell me that secret message! (The answer for this task starts from 'ructf\_')

## Other write-ups and resources

* <https://rdot.org/forum/showthread.php?t=3053&langid=1>
* <http://ahack.ru/write-ups/ructf-quals-14.htm>
* <http://hxp.io/blog/1/RuCTF%20Quals%202014:%20crypto500%20%22decrypt%20message%22/>
* <http://www.suslopas.pw/2014/03/ructf-crypto-500-decrypt-message.html>
