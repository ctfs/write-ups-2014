<!DOCTYPE html5>
<?php
function clean($n) {
   $n = htmlentities($n);
   $n = htmlspecialchars($n);
   $n = mysql_escape_string($n);
   return($n);
}

$_GET = array_map("clean", $_GET);
$_POST = array_map("clean", $_POST);
?>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Black Market</title>

    <!-- Le styles   -->
    <link href="assets/css/bootstrap.css" rel="stylesheet"/>
    <link href="assets/css/bootstrap-responsive.css" rel="stylesheet"/>
	<link href="assets/css/docs.css" rel="stylesheet"/>
	 
    <link href="style.css" rel="stylesheet"/>
	<link href="assets/js/google-code-prettify/prettify.css" rel="stylesheet"/>

	
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Le fav and touch icons -->
    <link rel="shortcut icon" href="assets/ico/favicon.ico">
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="assets/ico/apple-touch-icon-144-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="assets/ico/apple-touch-icon-114-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="assets/ico/apple-touch-icon-72-precomposed.png">
    <link rel="apple-touch-icon-precomposed" href="assets/ico/apple-touch-icon-57-precomposed.png">
  </head>
  <body>
  	<?php include('nav.php'); ?>
  	<div id="mainBody" class="container">
	<header id="header">
		<div class="row">
			<div class="span12">
				<a href="index.php"><img src="images/logo.png" alt="BlackMarket"/></a>
				<div class="pull-right"> <br/>
					<a href="view_cart.php"> <span class="btn btn-mini btn-warning"> <i class="icon-shopping-cart icon-white"></i></span> </a>
				</div>
			</div>
		</div>
		<div class="clr"></div>
	</header>