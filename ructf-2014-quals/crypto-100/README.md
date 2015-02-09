# RuCTF 2014 Quals: Crypto 100 - [Md5 lext](https://github.com/HackerDom/ructf-2014-quals/tree/master/tasks/md5_lext)

> Server (python27.quals.ructf.org:12337) accepts only authorized messages.
> It works like this:
>
<pre>
-------------------------------
	buf = c.recv(4096)
	digest, msg = buf.split(" ", 1)
	if (digest == md5(password+msg).hexdigest()):
		#here I send a secret
	else:
		c.send("Wrong signature\n")
-------------------------------
</pre>
>
> You have intercepted one authorized message: "b34c39b9e83f0e965cf392831b3d71b8 do test connection". Construct your own authorized message! Answer starts with 'RUCTF\_'

## Other write-ups and resources

* <http://xrekkusu.hatenablog.jp/entry/2014/03/11/214753>
* <https://ctfcrew.org/writeup/54>
* [Japanese](http://d.hatena.ne.jp/kusano_k/20140310/1394471922)
* <http://lights-out-ctf.ghost.io/ructf-2014-quals-crypto-100-md5/>
* <http://www.suslopas.pw/2014/03/ructf-crypto-100-md5.html>
