# DEFKTHON CTF: Recon 100

**Description:**

> [Francis Alexander](https://www.google.co.in/#q=Francis+Alexander)

## Write-up

Francis Alexander is a programmer who works for Opensec.

The flag is hidden on <http://wiredcreation.blogspot.in/2014/02/nosql-exploitation-framwework-released.html>. Inspect the DOM using your browser’s developer tools to look for HTML comments (note: plain view-source won’t work as the content is loaded through Ajax). You’ll eventually see this:

```html
<!-- flag{hmm_try_nosql_dbs_dude}-->
```

The flag is `hmm_try_nosql_dbs_dude`.

## Other write-ups

* none yet
