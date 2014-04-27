<?php

if(!isset($secret_salt,$database,$_COOKIE['auth']))
	return false;

$auth = $_COOKIE['auth'];
if(get_magic_quotes_gpc())
	$auth = stripslashes($auth);
$auth = unserialize($auth);

if(!is_array($auth))
	return false;

$auth['hmac_t'] = sha1(sha1($auth['username'].$auth['hmac_t'].$auth['password']).$secret_salt);

if($auth['hmac_t'] !== $auth['hmac'])
	return false;

$message = '';

foreach($database as $row)
{
	if($row['username'] == $auth['username']) 
	if($row['password'] == $auth['password'])
	{
		$message = $row['secret_message']; 
		return true;
	}
}

return false;