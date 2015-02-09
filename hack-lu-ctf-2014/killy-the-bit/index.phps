<?php
include 'config.php';

echo "<html><head><style type='text/css'><!-- body {background-image: url(bg.jpg);background-repeat: no-repeat;height: Percent;width: Percent; background-size: cover;}//--></style> <title>Royal Bank of Fluxembourg</title></head></html>";

<!-- blind? we will kill you :) -->
if(isset($_GET['name']) && $_GET['name']!='' && !preg_match('/sleep|benchmark|and|or|\||&/i',$_GET['name'])) {
	$res = mysql_query("SELECT name,email FROM user where name='".$_GET['name']."'");

	if(mysql_fetch_object($res)) {		
		// Generation of new password
		//<topsecure content>
		// this was filtered during the creation of the phps file
		//</topsecure content>
		die("A new password was generated and sent to your email address!");
	} else {


	$res = mysql_query("SELECT name,email FROM user where name sounds like '".$_GET['name']."'");

		if(mysql_fetch_object($res)) {
			echo "We couldn't find your username, but it sounds like this user:<br>";
		} else {
			die("We couldn't find your username!<br>Are you sure it is ".htmlspecialchars($_GET['name'],ENT_QUOTES, 'utf-8')."?");
		}
        $res = mysql_query("SELECT name,email FROM user where name sounds like '".$_GET['name']."'");

		while($row = mysql_fetch_object($res)) {
		   echo $row->name;
		   echo "<br>";
		}
	}
} else {

echo "<div style='width:800px; margin:0 auto;'><hr><h1><center>Royal Bank of Fluxembourg<center></h1><hr><br><br>Dear users,<br>We were hacked by Killy the Bit! Please use this site to generate your new password. Login will be available on the 23.10.2014 10:01 CEST<br><br><br></div>";
	 echo '<div style="width:400px;margin:0 auto;"<pre><img src=wanted.png></img></pre><br><br>';
	echo '<form action="#" method="get">Please enter your username: <br><input type="text" name="name"><br><input type="submit" name="submit" value="Generate"></form></div>';
}

?>
