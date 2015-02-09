<?php if (!defined('MAIN')) die();


$error = '';
$message = '';
if (!empty($_POST['name']) && !empty($_POST['pw'])) {
    if (!is_string($_POST['name']) || !is_string($_POST['pw'])) {
        $error = 'Wrong format.';
    } else {
        $query = $DB->prepare('INSERT INTO users (name, pw) VALUES (?, ?)');
        $query->execute(array($_POST['name'], sha1(SALT . $_POST['pw'])));
        $message = 'Registration complete: A sexy cow is waiting for your love, so log in right now!';
    }
} else {
    $error = 'Empty name or password.';
}


$t = new Template(TEMPLATE_DIR . 'message.pjson');
$t->assign(($error) ? $error : $message, 'message');
$t->assign(!$error, 'success');
$t->render();
