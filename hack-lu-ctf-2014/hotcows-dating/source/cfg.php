<?php if (!defined('MAIN')) die();


session_start();


/* Example configuration. Please change FLAG, SALT and the database credentials.
 * The database code expects one table (users):

CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),
                    pw VARCHAR(40), premium TINYINT DEFAULT 0,
                    support TINYINT DEFAULT 0);

CREATE TABLE reports (id INT AUTO_INCREMENT PRIMARY KEY, ip VARCHAR(255),
                      time INT, cow_name VARCHAR(255), area VARCHAR(255),
                      description TEXT);

 *
 * The send_to_ticket_system MUST and WILL be changed according to your ticket
 * and support system.
 */


define('INCLUDE_DIR', 'api/');
define('TEMPLATE_DIR', 'templates/');
define('JS_DIR', 'js/');
define('CSS_DIR', 'css/');


// change this
define('FLAG', 'XXX');
define('SALT', 'XXX');
$DB = new PDO('mysql:host=localhost;dbname=hotcows;charset=utf8', 'XXX', 'XXX');


define('XHR_HEADER', 'HTTP_X_REQUESTED_WITH');


header('Content-Type: text/html; charset=UTF-8');
header("Content-Security-Policy: default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'");
header('X-Frame-Options: DENY');


/**
 * Sends problem reports to an internal ticket system. A member of the support
 * team will visit the cow's profile and look for problems. Support uses the
 * newest version of Chromium.
 */
function send_to_ticket_system($cow_name, $area, $desc) {
    // Implementation deployment-specific
}
