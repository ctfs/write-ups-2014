# Sharif University Quals CTF 2014: Hidden Message

**Category:** Steganography
**Points:** 40
**Solves** 47
**Description:**

> What is the hidden message?
>
> [Download](hidden-message.pcap)

## Write-up

The pcap contains an UDP exchange with an excerpt of the [Classical Physics Wiki page](http://en.wikipedia.org/wiki/Classical_physics#Comparison_with_modern_physics).

We can extract the payload using this command:

```
$ tshark -r hidden-message.pcap -Tfields -e data | xxd -r -p
In contrast to classical physics modern physics is a slightly looser term which may refer to just quantum physics or to 20th and 21st century physics in general and so always includes quantum theory and may include relativity
A physical system on the classical level is a physical system in which the laws of classical physics are valid There are no restrictions on the application of classical principles but practically the scale of classical physics is the level of isolated atoms and molecules on upwards including the macroscopic and astronomical realm Inside the atom and among atoms in a molecule the laws of classical physics break down and generally do not provide a correct description
Moreover the classical theory of electromagnetic radiation is somewhat limited in its ability to provide correct descriptions since quantum effects are observable in more everyday circumstances than quantum effects of matter Unlike quantum physics classical physics is generally characterized by the principle of complete determinism although the Manyworlds interpretation of quantum mechanics is in a sense deterministic
Mathematically classical physics equations are ones in which Plancks constant does not appear According to the correspondence principle and Ehrenfests theorem as a system becomes larger or more massive action  Plancks constant the classical dynamics tends to emerge with some exceptions such as superfluidity This is why we can usually ignore quantum mechanics when dealing with everyday objects instead the classical description will suffice However one of the most vigorous ongoing fields of research in physics is classicalquantum correspondence This field of research is concerned with the discovery of how the laws of quantum physics give rise to classical physics in the limit of the large scales of the classical le
```
We can see that the last digit of the source port changes for each requests between the values of 0 and 1, so we try to extract that with `tshark` and evaluate the parsed digits using a quick `perl` binary to ascii converter:
```bash
$ tshark -r hidden-message.pcap -Tfields -e udp.srcport | while read port; do echo -n ${port: -1}; done | perl -lpe '$_=pack"B*",$_'
??????????
```

That's not quite it. Let's try to invert the binary output using `tr` before evaluating the binary output:

```bash
$ tshark -r hidden-message.pcap -Tfields -e udp.srcport | while read port; do echo -n ${port: -1}; done | tr 01 10 | perl -lpe '$_=pack"B*",$_'
Heisenberg
```

Success! The flag is `Heisenberg`!

## Other write-ups and resources

* <http://ctf.sharif.edu/2014/quals/su-ctf/write-ups/14/>
