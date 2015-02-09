<?php if (!defined('MAIN')) die();


$error = '';
$message = '';
if (!isset($_SESSION['premium']) || !isset($_SESSION['support'])) {
    $error = 'You are not logged in.';
} else if ($_SESSION['premium'] || $_SESSION['support']) {
    $message = 'PREM_' . FLAG;
} else {
    $error = 'Your account has not been upgraded to premium, yet.';
}


$t = new Template(TEMPLATE_DIR . 'message.pjson');
$t->assign(($error) ? $error : $message, 'message');
$t->assign(!$error, 'success');
$t->render();
