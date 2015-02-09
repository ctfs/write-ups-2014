#!/usr/bin/env node

// npm install express@3.18.0

var fs = require('fs')
var crypto = require('crypto')
var express = require('express')
var app = express()
app.listen(1409)
app.use(require('express').bodyParser({uploadDir: __dirname+'/upload_tmp/'}))

var HMAC_SECRET = ''
for (var i=0; i<20; i++) {
  HMAC_SΕCRET = HMAC_SECRET + (Math.random()+'').substr(2)
}

function hmac_sign(path) {
  var hmac = crypto.createHmac('sha256', HMAC_SECRET)
  hmac.update(path)
  return hmac.digest('hex')
}

app.get('/', function(req, res) {
  res.send('<!DOCTYPE html><html><head><title>docstore</title></head><body><ul>'
          +  '<li><a href="register">register</a></li>'
          +  '<li><a href="upload">upload a file</a></li>'
          +  '<li><a href="link">generate an access link</a></li>'
          +'</ul></body></html>')
})

function user_possible(user) {
  return /^[a-zA-Z]+$/.test(user)
}

function auth_ok(user, pass, cb) {
  if (!user_possible(user)) return cb(false)
  fs.readFile('users/'+user+'/pass', {encoding:'utf8'}, function(err, real_pass) {
    if (err) return cb(false) // e.g. if user doesn't exist
    cb(pass === real_pass)
  })
}

app.get('/register', function(req, res) {
  res.send('<!DOCTYPE html><html><head><title>register</title></head><body><form method="POST">'+
    'user: <input type="text" name="user"><br>pass: <input type="password" name="pass"><br><button type="submit">register</button>'+
    '</form></body></html>')
})

app.post('/register', function(req, res) {
  if (!req.body) return res.send('body missing? wtf?')
  var user = req.body.user, pass = req.body.pass;
  if (typeof user !== 'string' || typeof pass !== 'string') {
    return res.send('bad request')
  }

  if (!user_possible(user)) {
    return res.send('bad username')
  }

  var userdir = 'users/'+user+'/'
  fs.mkdir(userdir, function(err) {
    if (err) return res.send('unable to create user: '+e.code)
    fs.writeFile(userdir+'pass', pass, function(err) {
      if (err) throw err
      fs.mkdir(userdir+'files', function(err) {
        if (err) throw err
        res.redirect('/')
      })
    })
  })
})

app.get('/upload', function(req, res) {
  res.send('<!DOCTYPE html><html><head><title>upload</title></head><body><form method="POST" enctype="multipart/form-data">'+
    'user: <input type="text" name="user"><br>pass: <input type="password" name="pass"><br><input type="file" name="file"><br><button type="submit">upload</button>'+
    '</form></body></html>')
})

function sanitize_filename(f) {
  f = f.replace(/[^a-zA-Z0-9_.-]/g, '')
  if (f.length == 0 || f[0] == '.') f = '_'+f
  return f
}

app.post('/upload', function(req, res) {
  if (!req.body) return res.send('body missing? wtf?')
  var user = req.body.user, pass = req.body.pass, file = req.files.file;
  if (typeof user !== 'string' || typeof pass !== 'string' || typeof file !== 'object') {
    return res.send('bad request')
  }

  auth_ok(user, pass, function(is_ok) {
    if (!is_ok) return res.send('bad auth')
    var filename = sanitize_filename(file.name)
    fs.rename(file.path, 'users/'+user+'/files/'+filename, function(err) {
      if (err) return res.send('error: unable to rename')
      res.send('file was stored with name '+filename)
    })
  })
})

app.get('/link', function(req, res) {
  res.send('<!DOCTYPE html><html><head><title>generate a link</title></head><body><form method="POST" enctype="multipart/form-data">'+
    'user: <input type="text" name="user"><br>pass: <input type="password" name="pass"><br>file: <input type="text" name="file"><br><button type="submit">generate link</button>'+
    '</form></body></html>')
})

app.post('/link', function(req, res) {
  if (!req.body) return res.send('body missing? wtf?')
  var user = req.body.user, pass = req.body.pass, file = req.body.file;
  if (typeof user !== 'string' || typeof pass !== 'string' || typeof file !== 'string') {
    return res.send('bad request')
  }
  file = sanitize_filename(file)

  auth_ok(user, pass, function(is_ok) {
    if (!is_ok) return res.send('bad auth')
    file = file.replace(/[^a-zA-Z0-9_.-]/g, '')
    res.redirect('/files/'+user+'/'+file+'/'+hmac_sign(user+'/'+file))
  })
})

app.get('/files/:user/:file/:signature', function(req, res) {
  var user = req.params.user, file = req.params.file, signature = req.params.signature
  if (!user_possible(user)) return res.send('bad user')
  if (sanitize_filename(file) !== file) return res.send('bad filename')
  if (hmac_sign(user+'/'+file) !== signature) return res.send('bad signature')
  res.set('Content-Type', 'text/plain')
  res.sendfile('users/'+user+'/files/'+file)
})
