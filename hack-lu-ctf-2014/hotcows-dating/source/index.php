<?php


define('MAIN', 1);
require_once 'cfg.php';
require_once 'lib/util.php';
require_once 'lib/Template.php';


if (isset($_SERVER[XHR_HEADER]) && $_SERVER[XHR_HEADER] == 'XMLHttpRequest') {
    if (isset($_GET['api'])) {
        $page = 'error.php';
        if (is_string($_GET['api']) && preg_match('/^\w+\.php$/', $_GET['api'])
            && is_file(INCLUDE_DIR . $_GET['api'])) {
            $page = $_GET['api'];
        }
    }
    include INCLUDE_DIR . $page;
} else {
    $t = new Template(TEMPLATE_DIR . 'layout.phtml');
    $t->render();
}
