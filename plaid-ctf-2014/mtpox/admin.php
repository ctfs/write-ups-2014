<?php
  require_once("secrets.php");
  $auth = false;
  if (isset($_COOKIE["auth"])) {
     $auth = unserialize($_COOKIE["auth"]);
     $hsh = $_COOKIE["hsh"];
     if ($hsh !== hash("sha256", $SECRET . strrev($_COOKIE["auth"]))) {
       $auth = false;
     }
  }
  else {
    $auth = false;
    $s = serialize($auth);
    setcookie("auth", $s);
    setcookie("hsh", hash("sha256", $SECRET . strrev($s)));
  }
  if ($auth) {
    if (isset($_GET['query'])) {
      $link = mysql_connect('localhost', $SQL_USER, $SQL_PASSWORD) or die('Could not connect: ' . mysql_error());
      mysql_select_db($SQL_DATABASE) or die('Could not select database');
      $qstr = mysql_real_escape_string($_GET['query']);
      $query = "SELECT amount FROM plaidcoin_wallets WHERE id=$qstr";
      $result = mysql_query($query) or die('Query failed: ' . mysql_error());
      $line = mysql_fetch_array($result, MYSQL_ASSOC);
      foreach ($line as $col_value) {
        echo "Wallet " . $_GET['query'] . " contains " . $col_value . " coins.";
      }
    } else {
       echo "<html><head><title>MtPOX Admin Page</title></head><body>Welcome to the admin panel!<br /><br /><form name='input' action='admin.php' method='get'>Wallet ID: <input type='text' name='query'><input type='submit' value='Submit Query'></form></body></html>";
    }
  }
  else echo "Sorry, not authorized.";
?>
