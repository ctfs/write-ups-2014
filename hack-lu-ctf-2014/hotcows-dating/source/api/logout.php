<?php if (!defined('MAIN')) die();


$t = new Template(TEMPLATE_DIR . 'message.pjson');
if (isset($_SESSION['support']) && !$_SESSION['support']) {
    session_destroy();
    $t->assign('Successfully logged out.', 'message');
    $t->assign(true, 'success');
} else {
    $t->assign('Cannot log out as admin ;)', 'message');
    $t->assign(false, 'success');
}
$t->render();
