<?php if (!defined('MAIN')) die();


$t = new Template(TEMPLATE_DIR . 'message.pjson');
$t->assign('404 - Not Found.', 'message');
$t->assign(false, 'success');
$t->render();
