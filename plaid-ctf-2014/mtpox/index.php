<?
  if (isset($_GET['page'])) {
    if (strstr($_GET['page'], "secrets")) { echo "ERROR!\n"; }
    else { readfile(basename($_GET['page'])); }
  }
  else {
    readfile("index");
  }
?>
