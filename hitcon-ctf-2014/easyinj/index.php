<?php

if (!isset($_SESSION)) { session_start(); }
ini_set('display_errors',1);
error_reporting(E_ALL);


if(!isset($_REQUEST["ip"]))
{
header("Location: {$_SERVER['PHP_SELF']}?ip={$_SERVER['REMOTE_ADDR']}");

exit;
}
else
{
$_SESSION['sql']="1";

}

$ip = $_REQUEST['ip'];

PHPInfo2File("log_guess^2/{$_SERVER['REMOTE_ADDR']}");
$hostdb = 'localhost';
$namedb = 'log';
$userdb = 'root';
$passdb = '2o3tnowe@k';

$filter = 'UNION/SELECT/OUTFILE/DUMPFILE/OR/AND/NULL/WHERE/LOAD_FILE/INSERT/DELETE/CREATE/INTO/FROM/BENCHMARK';

$filter_arr = explode("/",$filter);

foreach($filter_arr as $filt)
{
$ip = str_ireplace($filt,'',$ip);
}

$ip = str_replace('.','',$ip);
if($_SESSION['sql'] == "1")
{

$conn = new PDO("mysql:host=$hostdb; dbname=$namedb", $userdb, $passdb, array(PDO::ATTR_PERSISTENT => true) );
$conn->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING );
$conn->query("INSERT INTO `log`.`log` values('{$ip}')");  

$ip = mysql_real_escape_string($ip);
$conn->query("INSERT INTO `log`.`log` values('{$ip}')");  
$conn = null;
$_SESSION['sql']="2";
}

phpinfo();
function PHPInfo2File($target_file){
     ob_start();
    phpinfo();
    $info = ob_get_contents();
    ob_end_clean();
 
    $fp = fopen($target_file, "a+");
    fwrite($fp, $info);
    fclose($fp);
}
?>