<?php if (!defined('MAIN')) die();


function http_redirect($location) {
    header('Location: ' . $location);
}
