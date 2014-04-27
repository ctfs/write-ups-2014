<?php
error_reporting(0);
$included = true;
require('secret.php');
require('database.php');
require('message.php');
$logged_in = require('auth.php');
?><!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="DS Teaser 2014: WEB400">
    <meta name="author" content="Dragon Sector">

    <title>WEB400</title>

    <link href="css/bootstrap.min.css" rel="stylesheet">

    <link href="css/jumbotron.css" rel="stylesheet">

  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Fiery Technologies</a>
        </div>
        <div class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" role="form" method="post" action="<?php echo ($logged_in?'logout.php':'login.php') ?>"><?php if(!$logged_in) { ?>
            <div class="form-group">
              <input type="text" placeholder="Username" class="form-control" name="user">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" class="form-control" name="pass">
            </div>
            <button type="submit" class="btn btn-success">Sign in</button><?php } else { ?>
				<button type="submit" class="btn btn-success">Logout</button><?php } ?>
          </form>
        </div>
      </div>
    </div>

    <div class="jumbotron">
      <div class="container">
<?php if(!$logged_in) { ?>        <h1>You're not logged in.</h1>
        <p>Welcome to our new security system. You can try the demo version of the script here. For sure you'll be pleased.</p>
		  <p>Use below credentials to try out our unbreakable message system:</p>
        <p><a class="btn btn-primary btn-lg" role="button">&laquo; guest:guest &raquo;</a></p>
		  <p>&nbsp;</p>
		  <p>We'll be looking forward your order.</p><?php } else printmsg($message,$auth['password']); ?>

      </div>
    </div>

    <div class="container">
      
      <hr>

      <footer>
        <p>&copy; Dragon Sector CTF Teaser 2014</p>
      </footer>
    </div>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>
