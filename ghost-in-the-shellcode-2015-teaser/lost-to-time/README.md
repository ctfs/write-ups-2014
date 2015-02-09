# Ghost in the Shellcode 2015 teaser: Lost to Time

**Description:**

> So I lost my computer. And also my compiler and most of the documentation. Can you help me, please?
>
> [File](losttotime-fe4ed7af5cefa136e2c72f67810b72b0de269a72cc2f61ce649f6d1ce759b396)

## Write-up

```bash
$ file losttotime-fe4ed7af5cefa136e2c72f67810b72b0de269a72cc2f61ce649f6d1ce759b396
losttotime-fe4ed7af5cefa136e2c72f67810b72b0de269a72cc2f61ce649f6d1ce759b396: xz compressed data

$ unxz < losttotime-fe4ed7af5cefa136e2c72f67810b72b0de269a72cc2f61ce649f6d1ce759b396 > losttotime

$ file losttotime
losttotime: ASCII text
```

The `losttotime` file has the following contents:

```
          IDENT     CTF
          ABS
          SST
          ENTRY     CTF
          SYSCOM    B1
          SPACE  4,10
          ORG    110B
 FWA      BSS    0

 BUFL     EQU    401B

 F        BSS    0
 ZZZZZG0  FILEB  FBUF,BUFL,DTY=2RTT

 CTF      BSS       0
          SB1       1
          SA1       CTFB
          BX6       X1
          SB7       27
          SA6       A1
          SA2       CTFA
          MX0       30
          SA1       A2+B1

 CTF2     BX6       X0*X1
          ZR        X6,CTF4
          JR        FCT
          SA6       A6+B1
          BX6       -X0*X1
          ZR        X6,CTF4
          JR        FCT
          SA6       A6+B1
          SA1       A1+B1
          NZ        X1,CTF2

 CTF4     WRITES    F,CTFB,CTFBL
          ENDRUN

 FCT      SUBR
          CX6       X6
          SB6       X6
          LT        B6,B7,FCT2
          SB6       B6-B7
          SB6       B6+B6
          SB5       B6+B6
          SB5       B5+B5
          SB6       B5+B6
          AX6       X2,B6
          MX7       -10
          BX6       -X7*X6
 FCT2     JP        FCTX

 CTFA     BSS       0
          VFD       6/00B,9/000B,9/000B,9/520B,9/244B,9/120B,9/057B
          VFD       6/40B,9/210B,9/003B,9/100B,9/774B,9/415B,9/040B
          VFD       6/00B,9/000B,9/400B,9/000B,9/442B,9/211B,9/001B
          VFD       6/77B,9/776B,9/777B,9/770B,9/010B,9/002B,9/004B
          VFD       6/77B,9/377B,9/577B,9/610B,9/040B,9/000B,9/400B
          VFD       6/00B,9/100B,9/200B,9/343B,9/556B,9/115B,9/671B
          VFD       6/00B,9/000B,9/004B,9/441B,9/625B,9/031B,9/752B
          VFD       6/63B,9/015B,9/236B,9/227B,9/165B,9/273B,9/762B
          VFD       6/27B,9/167B,9/713B,9/057B,9/111B,9/504B,9/353B
          VFD       6/14B,9/205B,9/324B,9/130B,9/006B,9/000B,9/100B
          VFD       6/67B,9/775B,9/673B,9/736B,9/000B,9/000B,9/000B
          VFD       6/10B,9/007B,9/000B,9/204B,9/666B,9/666B,9/661B
          VFD       6/10B,9/010B,9/010B,9/010B,9/002B,9/000B,9/000B
          VFD       6/35B,9/671B,9/077B,9/650B,9/001B,9/000B,9/000B
          VFD       6/70B,9/000B,9/000B,9/007B,9/677B,9/737B,9/566B
          VFD       6/40B,9/000B,9/000B,9/044B,9/000B,9/700B,9/004B
          VFD       6/57B,9/135B,9/427B,9/072B,9/000B,9/400B,9/010B
          VFD       6/54B,9/710B,9/650B,9/722B,9/667B,9/170B,9/671B
          VFD       6/37B,9/503B,9/354B,9/061B,9/653B,9/521B,9/704B
          VFD       6/67B,9/531B,9/564B,9/700B,9/000B,9/000B,9/004B
          VFD       6/12B,9/345B,9/677B,9/674B,9/127B,9/002B,9/011B
          VFD       6/27B,9/315B,9/340B,9/647B,9/003B,9/653B,9/700B
          VFD       6/77B,9/777B,9/777B,9/770B,9/000B,9/000B,9/000B
          VFD       6/00B,9/000B,9/000B,9/000B,9/000B,9/000B,9/055B
 CTFB     BSS       0
          DUP       64,1
          DATA      1R
 CTFBL    EQU       *-CTFB

 COMCPL   XTEXT     COMCCDD
 COMCPL   XTEXT     COMCCIO
 COMCPL   XTEXT     COMCCPM
 COMCPL   XTEXT     COMCDXB
 COMCPL   XTEXT     COMCLFM
 COMCPL   XTEXT     COMCSYS
 COMCPL   XTEXT     COMCWTS
 COMCPL   XTEXT     COMCWTW
 BUFFERS  SPACE     4,10
          USE       BUFFERS
 FBUF     EQU       *
 RFL=     EQU       FBUF+BUFL+10

          END
```

(TODO)

## Other write-ups and resources

* <https://sushant94.github.io/2014/12/15/gits_teaser_writeup/>
* <https://wwwcip.cs.fau.de/~hu78sapy/pdf/gits_teaser.pdf>
