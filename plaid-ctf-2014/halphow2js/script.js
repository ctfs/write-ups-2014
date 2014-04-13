var FLAG="XXXXXXXXXXXXXXXXXXXXXX"; // <- Try submitting that, I dare you.

// JJJJJJJJJJJAAAAAAAAAAAAVVVVVVVVVVAAAAAAAAAAAASSSSSSSSSSCCCCCCCCCCCRRRRRRRRRRIIIIIIIIIIPPPPPPPPPPPPPTTTTTTTTTTTTT

function mystop(z) {
for(var xxx = 5; xxx < 50; xxx+=5) {
	var yyy = (function stopb(b) { return b < 0 ? function(n){return Infinity;} : function stop(n) {
	return (function(s){return s && (s<b?s:Infinity)})(mystop.sbox[n]) || (function(q){return q == Infinity ? q : (mystop.sbox[n] = q)})(1+Math.min.apply(null, [n/2, 3*n+1, n/(function twos(n) {
		return n%2 || 2*twos(n/2);
	})(n)].map(function xia(x,i,a) {
		return i >= a.length ? undefined : x%1 || !x || x == n ? (function(){a.splice(i,1); return xia(a[i],i,a);})() : x;
	}).filter(function(x){return x;}).map(stopb(b-1))));
	// i'll make a JAVASCRIPT problem SO HARD that EVEN MATH CAN'T SOLVE IT
}; })(xxx)(z);
	if(yyy != Infinity) return yyy;
}
}
mystop.sbox = {2:1, 1:1, 4:1};

function filter() {
	var args = [].slice.apply(arguments).sort().filter(function(x,i,a){return a.indexOf(x) == i;});
	if(args.length != 5) return "uniq";
	
	var flag = false; args.map(function(x){flag |= x >= 999;});
	if(flag) return "big";
	
	var m = args.map(mystop);
	
	if(m.filter(function(x,i){return m[2]+3*i == x;}).length < 3) return "unsexy";
	if(m.filter(function(x,i){return x == args[i];}).length < 3) return "hippopotamus";
	if(m.filter(function(x,i){return x > m[i-1];}).length > 3) return "banana phone";
	
	return FLAG;
}

function self_test() {
	// SLOW SLOW SLOW self test
	var checksum1 = 15661;
	var checksum2 = 19;
	var i = 999;
	while(--i > 0) {
		var x = mystop(i);
		if(!(0 < x && x < 50)) return false;
		checksum1 -= x;
		checksum2 ^= x;
	}
	return checksum1 === 0 && checksum2 === 0;
}

function client_side() {
	var x,y,z,w,ww;
	while(1) {
		x = prompt("#1", '1'); if(!x) return;
		y = prompt("#2", '2'); if(!y) return;
		z = prompt("#3", '3'); if(!z) return;
		w = prompt("#YOLO", '420'); if(!w) return;
		ww = prompt("#PPP", '123'); if(!ww) return;
		
		// The best solutions run FAST!
		// So, skip the slow self test if you've got a solution!
		if(filter(x,y,z,w,ww) == FLAG) break;
		
		if(!self_test()) {
			alert("Sanity check failed! Get a better javascript!");
			return;
		}
		alert("Pick better numbers, man.");
	}
	call_server(x,y,z,w,ww, function(x) { alert(x); });
}

function call_server(x,y,z,w,ww,handler) {
	xmlhttp = new XMLHttpRequest();
	var port = "80"
	if(document.location.port) port = document.location.port;
	xmlhttp.open("GET", "https://"+document.location.hostname+":"+port+ // arrr, where be my C format stringsss
	             "/myajax?x="+x+"&y="+y+"&z="+z+"&w="+w+"&ww="+ww, true); // CSTYLE4LYFE
	xmlhttp.onreadystatechange = function(){
		if(xmlhttp.readyState==4 && xmlhttp.status==200) {
			handler(string=xmlhttp.responseText);
		}
	}
	xmlhttp.send();
}
// JJJJJJJJJJJAAAAAAAAAAAAVVVVVVVVVVAAAAAAAAAAAASSSSSSSSSSCCCCCCCCCCCRRRRRRRRRRIIIIIIIIIIPPPPPPPPPPPPPTTTTTTTTTTTTT

// NNNNNNNNNNOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEEEEEEEEEEEEEEE
function server_side() {
	var server_cache = require('./server_cache.js');
	FLAG = require('./server_flag.js').FLAG; // scripte flage
	var https = require('https');
	var fs = require('fs');
	var url = require('url');

	https.createServer({
		key: fs.readFileSync('./key.pem'),
		cert: fs.readFileSync('./cert.pem')
	}, function(request, response) {
		var location = url.parse(request.url, true);
		var path = location.pathname;
		var query = location.query;
		
		var respondWithFile = function(path, type) {
			fs.readFile(path, function(err, file) {
				if(err) {
					response.writeHead(500, { 'Content-Type': 'text/plain' });
					response.end('five double oh', "utf-8"); 
					return;
				}  
				response.writeHead(200, { 'Content-Type': type ? type : 'text/plain' });
				response.end(file, "utf-8");
			});
		}
	
		if(path==="/myajax") {
			console.log(url.parse(request.url, false).query); // lol what R U n00bs sending, anyways
			setTimeout(function() {
				
				///////////////////////////////////
				mystop.sbox = server_cache.sbox; // Don't run the server into the ground, kthxbai
				/////////////////////////////////// Server would logically be the same with or without this.
				
				if(!self_test()) {
					response.writeHead(500, {"Content-Type": "text/plain"});
					response.end("nigga, I AM BROKE", "utf-8");
				}
				
				response.writeHead(200, {"Content-Type": "text/plain"});
				
				var fff = "nope";
				try {
					fff = filter(query.x, query.y, query.z, query.w, query.ww);
				} catch(e) {}
				var sss = "CHEATER :P. Ping clockish if you can:\n";
				sss += "\t1. Visit this site, unmodified, NOTHING PATCHED OUT, in Chrome.\n";
				sss += "\t2. Enter numbers in USING THE DIALOG BOXES that pop up. No manual calls!\n";
				sss += "\t3. Somehow still manage to see this response from the server.\n";
				sss += "It shouldn't be possible, but then again I have no idea what I'm doing.";
				// OH MY GOD WHAT IS JAVASCRIPT WHERE AM I WHAT IS NODE HALP HOW 2 JS
				response.end(fff == FLAG ? FLAG : sss, "utf-8");
			}, 2000);
		}
		else if(path==="/" || path==="/index.html") {
			respondWithFile('./index.html', 'text/html');
		}
		else if(path==="/script.js") { 
			respondWithFile('./script.js', 'text/javascript'); // This file is me! Haaiii!
		}
		else if(path==="/server_flag.js") {
			response.writeHead(401, {"Content-Type": "text/plain"});
			response.end("nowaaaaiii");
		}
		else if(path==="/server_cache.js") {
			// respondWithFile('./server_cache.js', 'text/javascript');
			// return;
			response.writeHead(401, {"Content-Type": "text/plain"});
			response.end("I bet y'all wish you knew MATH or JAVASCRIPT or SOMETHING.");
		}
		else {
			response.writeHead(404, { 'Content-Type': 'text/html' });
			response.end("four oh four", "utf-8");
		}
	}).listen(8001);
}

try {document;} catch(ReferenceError) {server_side();}
// NNNNNNNNNNOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEEEEEEEEEEEEEEE
