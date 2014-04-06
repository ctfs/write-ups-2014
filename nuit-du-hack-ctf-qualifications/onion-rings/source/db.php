<?php
	function db_connect()
	{
	// Initialize connection variables
	$dbhost = "localhost";
	$dbname = "black_market";
	$dblogin = "blackmarket";
	$dbpass = "Bl4km4rk3t";

	// Connect to the database
		try
		{
			$bdd = new PDO('mysql:host='.$dbhost.';dbname='.$dbname.'',$dblogin,$dbpass);
		}
		catch(Exception $e)
		{
			die('Erreur: ' . $e->getMessage());
		}
		return $bdd;
	}
	?>