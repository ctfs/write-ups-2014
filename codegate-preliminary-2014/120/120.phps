<?php
session_start();

$link = @mysql_connect('localhost', '', '');
@mysql_select_db('', $link);

function RandomString()
{
  $filename = "smash.txt";
  $f = fopen($filename, "r");
  $len = filesize($filename);
  $contents = fread($f, $len);
  $randstring = '';
  while( strlen($randstring)<30 ){
    $t = $contents[rand(0, $len-1)];
    if(ctype_lower($t)){
    $randstring .= $t;
    }
  }
  return $randstring;
}

$max_times = 120;

if ($_SESSION['cnt'] > $max_times){
  unset($_SESSION['cnt']);
}

if ( !isset($_SESSION['cnt'])){
  $_SESSION['cnt']=0;
  $_SESSION['password']=RandomString();

  $query = "delete from rms_120_pw where ip='$_SERVER[REMOTE_ADDR]'";
  @mysql_query($query);

  $query = "insert into rms_120_pw values('$_SERVER[REMOTE_ADDR]', '$_SESSION[password]')";
  @mysql_query($query);
}
$left_count = $max_times-$_SESSION['cnt'];
$_SESSION['cnt']++;

if ( $_POST['password'] ){
  
  if (eregi("replace|load|information|union|select|from|where|limit|offset|order|by|ip|\.|#|-|/|\*",$_POST['password'])){
    @mysql_close($link);
    exit("Wrong access");
  }

  $query = "select * from rms_120_pw where (ip='$_SERVER[REMOTE_ADDR]') and (password='$_POST[password]')";
  $q = @mysql_query($query);
  $res = @mysql_fetch_array($q);
  if($res['ip']==$_SERVER['REMOTE_ADDR']){
    @mysql_close($link);
    exit("True");
  }
  else{
    @mysql_close($link);
    exit("False");
  }
}

@mysql_close($link);
?>

<head>
<link rel="stylesheet" type="text/css" href="black.css">
</head>

<form method=post action=index.php>
  <h1> <?= $left_count ?> times left </h1>
  <div class="inset">
  <p>
    <label for="password">PASSWORD</label>
    <input type="password" name="password" id="password" >
  </p>
  </div>
  <p class="p-container">
    <span onclick=location.href="auth.php"> Auth </span>
    <input type="submit" value="Check">
  </p>
</form>