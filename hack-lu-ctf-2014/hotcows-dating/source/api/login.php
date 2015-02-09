<?php if (!defined('MAIN')) die();


$error = '';
$message = '';
if (empty($_SESSION['id'])) {
    if (!empty($_POST['name']) && !empty($_POST['pw'])) {
        if (!is_string($_POST['name']) || !is_string($_POST['pw'])) {
            $error = 'Wrong format.';
        } else {
            $query = $DB->prepare('SELECT id, name, premium, support FROM users WHERE BINARY name=? AND pw=?');
            $query->execute(array($_POST['name'], sha1(SALT . $_POST['pw'])));
            if ($query->rowCount() > 0) {
                $result = $query->fetchObject();
                $_SESSION['id'] = $result->id;
                $_SESSIOn['name'] = $result->name;
                $_SESSION['premium'] = $result->premium;
                $_SESSION['support'] = $result->support;
                $message = 'Successfully logged in.';
            } else {
                $error = 'Wrong username or password.';
            }
        }
    } else {
        $error = 'Empty name or password.';
    }
} else {
    $error = 'Already logged in.';
}


$t = new Template(TEMPLATE_DIR . 'message.pjson');
$t->assign(($error) ? $error : $message, 'message');
$t->assign(!$error, 'success');
$t->render();
