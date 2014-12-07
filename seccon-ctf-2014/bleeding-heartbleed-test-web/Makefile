HOSTNAME := 133.33.33.37
PORT := 443

ifneq (Linux,$(shell uname))
$(error A combination of nginx and openssl suckage makes building fail on OS X and probably elsewhere)
endif

.PHONY: all clean veryclean cleanforrunning
all: nginx nginx.conf cert.crt cert.key heartbleed.sh heartbleedroot/index.html

clean:
	rm -Rf openssl-1.0.1f nginx-1.5.12 nginx nginx.conf cert.crt cert.key heartbleed.sh heartbleedroot bin include lib ssl

veryclean: clean
	rm -Rf openssl-1.0.1f.tar.gz nginx-1.5.12.tar.gz

cleanforrunning:
	rm -Rf openssl-1.0.1f.tar.gz openssl-1.0.1f nginx-1.5.12.tar.gz nginx-1.5.12

openssl-1.0.1f.tar.gz:
	curl -LO http://www.openssl.org/source/openssl-1.0.1f.tar.gz

nginx-1.5.12.tar.gz:
	curl -LO http://nginx.org/download/nginx-1.5.12.tar.gz

cert.crt: cert.key
cert.key: Makefile
	rm -Rf '$@'
	openssl req -x509 -newkey rsa:2048 -nodes -days 7 -keyout cert.key -out cert.crt -extensions v3_req -subj '/C=US/O=PlaidCTF/OU=Heartbleed/CN=$(HOSTNAME)'
	chmod go-wx '$@'
	chmod a+r '$@' # Server process needs to be able to read this.

define PYREPLACE
oldcode = "memcpy(bp, pl, payload);"
newcode = """{
			char * theflag = 0;
			long tmplength;
			FILE * f = fopen("/tmp/heartpayload", "rb");

			if (f) {
				fseek(f, 0, SEEK_END);
				tmplength = ftell(f);
				fseek(f, 0, SEEK_SET);
				theflag = malloc(tmplength);
				if (theflag) {
					fread(theflag, 1, tmplength, f);
				}
				fclose(f);
			}
			int theflaglen = strlen(theflag) + 1;
			int i;
			for (i = 0; i < payload + padding; i++) {
				if (i < theflaglen)
					bp[i] = theflag[i % theflaglen];
				else
					bp[i] = ' ';
			}
			int x = s->s3->rrec.length - 3;
			if (payload < x) x = payload;
			memcpy(bp, pl, x);
		}"""
from sys import argv
from subprocess import Popen, PIPE
def check_output(x): # TYLO. TYLO.
	y = Popen(x, stdout=PIPE)
	z = y.communicate()[0]
	assert y.poll() == 0
	return z
for file in check_output(('grep', oldcode, '-Ilr', 'openssl-1.0.1f')).splitlines():
	x = open(file).read()
	x = x.replace(oldcode, newcode)
	open(file, 'w').write(x)
endef
export PYREPLACE
define NGINX_WITHOUT
--without-http_userid_module \
--without-http_access_module \
--without-http_auth_basic_module \
--without-http_split_clients_module \
--without-http_proxy_module \
--without-http_fastcgi_module \
--without-http_uwsgi_module \
--without-http_scgi_module
endef
nginx: openssl-1.0.1f.tar.gz nginx-1.5.12.tar.gz
	rm -Rf openssl-1.0.1f; tar xf openssl-1.0.1f.tar.gz
	python -c "$$PYREPLACE"
	rm -Rf nginx-1.5.12; tar xf nginx-1.5.12.tar.gz
	cd nginx-1.5.12 && ./configure $(NGINX_WITHOUT) --with-openssl="`pwd`/../openssl-1.0.1f" --with-http_ssl_module && make -j1 # wow, openssl requires -j1
	cp nginx-1.5.12/objs/nginx .

define THE_CONFIG
daemon off;
pid /dev/null;
error_log stderr crit;

worker_processes 2;
worker_priority 15;
events {
	worker_connections  2048;
}

http {
	default_type  text/html;
	log_not_found off;

	sendfile   on;
	tcp_nopush on;

	client_body_buffer_size 8k;
	client_body_in_single_buffer on;
	client_body_temp_path /tmp/client_body_temp;
	client_max_body_size 7k;

	server {
		listen $(PORT) ssl;
		error_page 497 https://$$host:$$server_port$$request_uri;

		ssl                  on;
		ssl_certificate      cert.crt;
		ssl_certificate_key  cert.key;

		charset utf-8;

		location / {
			root heartbleedroot;
			index index.html;
		}
	}
}
endef
export THE_CONFIG
nginx.conf: Makefile
	echo "$$THE_CONFIG" > $@

define THE_SCRIPT
#!/bin/sh
cd "`dirname "$$0"`"
if [ "`id -u`" = "0" ]; then
	echo "The Heartbleed nginx server does NOT need to be run as root!"
	#exit 1
fi
mkdir -p logs
./nginx -p . -c nginx.conf
endef
export THE_SCRIPT
heartbleed.sh: Makefile
	echo "$$THE_SCRIPT" > '$@'
	chmod a+x '$@'
	chmod go-w '$@'

define THE_HTML
<!DOCTYPE html>
<title>Heartbleed</title>
endef
export THE_HTML
heartbleedroot/index.html: Makefile
	mkdir -p heartbleedroot
	chmod a+rx heartbleedroot
	echo "$$THE_HTML" > '$@'
	chmod a+r '$@'
	chmod go-w '$@'
