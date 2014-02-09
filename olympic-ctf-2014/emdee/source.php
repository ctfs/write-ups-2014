<html>
<head>
<title>Emdee</title>
<style type='text/css'>
body { font-family: Verdana, sans-serif; font-size: 15px; }
em { font-family: monospace; font-style: normal; font-weight: bold; padding: 4px 10px; background: #eee; border: 1px solid #aaa; }
strong { color: #800000; }
</style>
</head>
<body><center>
<h2>Welcome to Emdee</h2>
Welcome to the Emdee service. We use the famous <a href='http://www.ietf.org/rfc/rfc1321.txt'>MD5</a> algorithm to help keep your data secret.<p/>
MD5 is a one-way function, but it has a flaw: one can precompute a ton of MD5 hashes and make a rainbow table.<p/>
To mitigate this, we compute <em>MD5( SALT + your_secret )</em> (patent pending).<br/><br/>

<h3>See for yourself</h3>
We took a short dictionary word, fed it into our <b>genuine patent-pending algorithm</b> and got:<p/>
<em>40288d60073775070a7edcdcd1df9c56  -</em>.<p/>
Can you restore our secret word? We don't think so!<br/><br/>

<h3>Try for yourself</h3>
<strong>As for our FREE service, current timestamp will be added to your_secret</strong><br/>
Purchase the paid package to get rid of timestamp and to use our <b>genuine patent-pending algorithm</b>.<p/>
<big><form method='POST'>Secret: <input type='password' name='secret' /> <input type='submit' value='&raquo;' /></form></big>
<?php
$salt = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

if (isset($_POST['secret']) && $_POST['secret'] != "") {
  echo "Result: ";

  $timestamp = microtime(true);

  $descriptorspec = array(
     0 => array("pipe", "r"),
     1 => array("pipe", "w"),
     2 => array("pipe", "w")
  );
  $proc = proc_open('socat - exec:md5sum,pty,ctty,echo=0', $descriptorspec, $pipes);
  if (!$proc) {
    echo "<strong>Error occured</strong>";
  } else {
    $data = "$salt" . $_POST['secret'] . $timestamp . "\x04\x04";
    if (fwrite($pipes[0], $data) != strlen($data)) {
      echo "<strong>Error occured</strong>";
    }
    $res = "";
    while (!feof($pipes[1])) {
      $res .= fgetc($pipes[1]);
    }
    echo "MD5( SALT + your_secret + $timestamp ) = <em>" . htmlspecialchars(trim($res)) . "</em>";
  }
}
?>
</center></body>
</html>
