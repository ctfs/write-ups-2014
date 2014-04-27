<?php

function printmsg($message,$pwd)
{
	$mod = gmp_init('fffffffdffffffffffffffffffffffff',16);
	$mul = gmp_init('b562a81099dff41937c5ae51ba7427a4',16);
	$key = str_repeat(sprintf('%04x',crc32($pwd)&0xffff),8);
	$key = gmp_init($key,16);
	$pwd = gmp_init($pwd,16);
	
	for($i=0;$i<strlen($message);$i+=32)
	{
		$msg = substr($message,$i,32);
		$msg = gmp_init($msg,16);
		$msg = gmp_add($msg,$pwd);
		$msg = gmp_mul($msg,$mul);
		$msg = gmp_add($msg,$key);
		$msg = gmp_mod($msg,$mod);
		$msg = gmp_strval($msg,16);
		$msg = str_pad($msg,32,'0',STR_PAD_LEFT);
		$msg = pack('H*',$msg);
		echo $msg;
	}
}