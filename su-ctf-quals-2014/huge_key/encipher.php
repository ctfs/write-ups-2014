<?php
	$plaintext = file_get_contents("flag.txt");

	$key = "\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0";
	$hugekey = file_get_contents("hugekey.bin");
	foreach (str_split($hugekey, 2) as $block)
		for ($j = 0; $j < 2; $j++)
			$key[$j] = chr(ord($block[$j]) ^ ord($key[$j]));

	$iv_size = mcrypt_get_iv_size(MCRYPT_RIJNDAEL_128, MCRYPT_MODE_CBC);
	$iv = mcrypt_create_iv($iv_size, MCRYPT_RAND);

	$ciphertext = mcrypt_encrypt(MCRYPT_RIJNDAEL_128, $key, $plaintext, MCRYPT_MODE_CBC, $iv);

	$ciphertext = $iv . $ciphertext;
	file_put_contents("ciphertext.bin", $ciphertext);
?>