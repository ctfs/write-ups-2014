var express = require('express');
var swig = require('swig');
var url = require('url');
var fs = require('fs');
var child_process = require('child_process');
var path = require('path');
var async = require('async');

var app = express();
app.use('/css', express.static('css'));
app.use('/images', express.static('images'));

app.get('/', function(request, response) {
  response.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
  var params = url.parse(request.url, true).query || {};
  var options = filterOptions(params);

  getPosts(options.lang, function(results) {
    var template = swig.compileFile('/var/www/site/templates/index.html');
    response.write(template({
      lang: options.lang,
      posts: results,
      more: getProp(options.lang, 'more'),
      title: getProp(options.lang, 'title'),
      subtitle: getProp(options.lang, 'subtitle'),
      main_page: true
    }));

    response.end();
  });
});

app.get('/post/:post_name', function(request, response) {
  response.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
  var post_name = request.params.post_name.replace(/_/g, ' ');
  var params = url.parse(request.url, true).query || {};
  var options = filterOptions(params);

  getFileContents(getProp(options.lang, 'dir'), post_name + '.txt', function(err, content) {
    if (content) {
      var template = swig.compileFile('/var/www/site/templates/post.html');
      response.write(template({
        title: getProp(options.lang, 'title'),
        subtitle: getProp(options.lang, 'subtitle'),
        post_name: post_name,
        content: content.toString(),
        main_page: false,
        lang: options.lang
      }));
    }

    response.end();
  });
});

function filterOptions(params) {
  var options = {}

  var sorted_param_names = Object.keys(params).sort();
  var params_processed = 0;
  for (i = 0; i < sorted_param_names.length; i++) {
    var lowered = sorted_param_names[i].toLowerCase();

    if (lowered == 'lang') {
      filterValidLanguages(params, lowered);
      options['lang'] = params[sorted_param_names[i]];
      params_processed++;
    // } else if (lowered == 'paginationnumposts') {
    //   param = params[sorted_param_names[i]];
    //   if (parseInt(param) > 0) {
    //     options['pagination_num_posts'] = parseInt(param);
    //     params_processed++;
    //   }
    } else {
      // Track user activity, so we can see where they go
      options['usertoken'] = params[sorted_param_names[i]];
      params_processed++;
    }

    if (params_processed >= 3) return options;
  }
  return options;
}

function getPosts(locale, callback) {
  var dir = getProp(locale, 'dir');

  // Make sure dates are correctly localised
  var env = process.env;
  env['LC_ALL'] = locale;
  child_process.exec('ls -l ' + dir, {env: env}, function(err, stdout) {
    var files = stdout.split('\n');
    var results = [];
    if (files.length > 0) {
      // Remove ls header and trailer
      files = files.slice(1, -1);
      async.map(files, function (file, callback) {
        var filename = file.substr(45);
        var modified_date = file.substr(32, 12);

        getFileContents(dir, filename, function(err, content) {
          // On error, resume next
          if (err) {
            callback(null, null);
          } else {
            callback(null, {
              name: filename.slice(0, -4),
              summary: content.toString().substr(0, 300) + '...',
              modified: modified_date
            });
          }
        });
      }, function(err, results) {
        callback(results.filter(function(arg) {return arg}));
      });
    }
  });
}

function getProp(lang, prop) {
  if (lang == 'fr_FR') {
    props = {
      'more': 'Lire plus',
      'dir': '/var/www/site/posts_fr',
      'title': 'Nébuleuse',
      'subtitle': "Voyages d'une étoile solitaire"
    }
  // } (lang == 'ru_RU') {
  //   props = {
  //     'more': 'прочитайте больше',
  //     'dir': '/var/www/site/posts_ru',
  //     'title': 'гроза',
  //     'subtitle': "В Советской России ..."
  //   }
  } else {
    props = {
      'more': 'Read more',
      'dir': '/var/www/site/posts_en',
      'title': 'Cumulonimbus',
      'subtitle': 'Travels of a lonely cloud'
    }
  }
  return props[prop];
}

function getFileContents(dir, filename, callback) {
  if (filename.length == 0) {
    callback('You must pass a filename');
  } else {
    var full_path = path.join(dir, filename);
    if (full_path.indexOf(dir) !== 0) throw('Villains!');
    fs.readFile(full_path, function (err, data) {
      if (err) {
        callback(err);
      } else {
        callback(null, data.toString());
      }
    });
  }
}

function filterValidLanguages(params, param_name) {
  // Russian doesn't work on this server for some reason?
  // LANGUAGES = ['fr_FR', 'en_US', 'ru_RU']
  var LANGUAGES = ['fr_FR', 'en_US']
  for (i = 0; i < LANGUAGES.length; i++) {
    if (params[param_name] == LANGUAGES[i]) return;
  }
  params[param_name] = 'en_US';
  return;
}

app.listen(8888, '0.0.0.0');

