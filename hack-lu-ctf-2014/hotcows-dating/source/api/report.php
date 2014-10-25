<?php if (!defined('MAIN')) die();


$error = '';
$message = '';
$ip = (array_key_exists('HTTP_X_FORWARDED_FOR', $_SERVER)) ? $_SERVER['HTTP_X_FORWARDED_FOR'] : $_SERVER['REMOTE_ADDR'];
if (!empty($_POST['cow_name']) && isset($_POST['area']) && !empty($_POST['desc'])) {
    if (!is_string($_POST['cow_name']) || !is_string($_POST['area']) || !is_string($_POST['desc'])) {
        $error = 'Wrong format.';
    } else {
        $query = $DB->prepare('SELECT id FROM reports WHERE ip=? AND time>UNIX_TIMESTAMP()-180');
        $query->execute(array($ip));
        if ($query->rowCount() > 0) {
            $error = 'You are only allowed to send reports every 3 minutes. Please be patient with our slow support team.';
        } else {
            $query = $DB->prepare('INSERT INTO reports (ip, time, cow_name, area, description) VALUES (?, UNIX_TIMESTAMP(), ?, ?, ?)');
            $query->execute(array($ip, $_POST['cow_name'], $_POST['area'], $_POST['desc']));
            send_to_ticket_system($_POST['cow_name'], $_POST['area'], $_POST['desc']);
            $message = "Your report has been forwarded to the support team. The cow's profile will be looked at very soon.";
        }
    }
} else {
    $error = 'No data given.';
}


$t = new Template(TEMPLATE_DIR . 'message.pjson');
$t->assign(($error) ? $error : $message, 'message');
$t->assign(!$error, 'success');
$t->render();
