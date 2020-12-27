<?php
/*
 Enable gzip
 */
ob_start('ob_gzhandler');
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', "borstvoedingoostbrabant_nl_wordpress");
/** MySQL database username */
define( 'DB_USER', "borstvoedingoostbrabant_nl_wordpress");
/** MySQL database password */
define( 'DB_PASSWORD', "K688fdRRviXz");
/** MySQL hostname */
define( 'DB_HOST', "localhost");
/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8');
/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '');
/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '8845e746aaece75bd07958667500452196bbcdee');
define( 'SECURE_AUTH_KEY',  '5e208ae9d5b81e9e4bf208d2f2aae9cb3e4b5be8');
define( 'LOGGED_IN_KEY',    'fa90f172952e32256aac71daf0a1738c8b6e76e4');
define( 'NONCE_KEY',        '78aff3e5589e9d70d14a0b50bd5be114a1bd5522');
define( 'AUTH_SALT',        '222fb4e493ce5c807789711beb94b87225494b77');
define( 'SECURE_AUTH_SALT', '9916419b6ba3cdee6b2bb3249c8c9f68d8759c16');
define( 'LOGGED_IN_SALT',   'e24f4f89c5db9ec1f672df524c537726bec6cebd');
define( 'NONCE_SALT',       '844dd7dbe115071f1fa0560988ab4d89b34fda62');
/**#@-*/
/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';
/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );
/**
 * These settings were added by TransIP for your ease
 */
define('FTP_USER', 'borstvoedingoostbrabant.nl');
define('FTP_HOST', 'ftp.borstvoedingoostbrabant.nl');
define('FTP_SSL', false);
if (isset($_SERVER['HTTP_X_TRANSIP_TRANSURL'])) {
    define('WP_SITEURL', 'http://' . $_SERVER['HTTP_HOST'] . '.transurl.nl');
    define('WP_HOME', 'http://' . $_SERVER['HTTP_HOST'] . '.transurl.nl');
} else {
    define('WP_SITEURL', 'https://' . $_SERVER['HTTP_HOST']);
    define('WP_HOME', 'https://' . $_SERVER['HTTP_HOST']);
}
define('FS_METHOD', 'direct');
/* That's all, stop editing! Happy publishing. */
/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}
/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
/** TransIP fix: sendmail does not support flags. This fix is needed in order to make mailing work. */
global $phpmailer;
if ((!is_object( $phpmailer ) || !is_a( $phpmailer, 'PHPMailer' )) &&
     file_exists(ABSPATH . '/wp-includes/class-phpmailer.php') &&
     file_exists(ABSPATH . '/wp-includes/class-smtp.php')) {
	require_once ABSPATH . '/wp-includes/class-phpmailer.php';
	require_once ABSPATH . '/wp-includes/class-smtp.php';
	$phpmailer = new PHPMailer( true );
}
$phpmailer->UseSendmailOptions = false;

