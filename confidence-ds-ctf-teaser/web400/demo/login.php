<?php

function denied()
{
	header('Location: index.php');
	exit();
}

function salt()
{
	$charset = '0123456789abcdef';
	$length = 16;
	$salt = '';
	while($length--)
		$salt .= $charset[rand() % 16];
	return $salt;
}

require('secret.php');
require('database.php');

if(!isset($_POST['user'],$_POST['pass']))
	denied();

$user = (string)$_POST['user'];
$pass = (string)$_POST['pass'];
$pass = md5($pass);

$success = false;

foreach($database as $row)
{
	if($row['username'] == $user) 
	if($row['password'] == $pass)
		$success = true;
}

if(!$success)
	denied();

$salt = salt();
$sign = sha1(sha1($user.$salt.$pass).$secret_salt);
$auth = array(
	'username' => $user,
	'password' => $pass,
	'hmac_t'   => $salt,
	'hmac'     => $sign
);

setcookie('auth',serialize($auth));

header('Location: index.php');