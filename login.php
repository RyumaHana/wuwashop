<?php
require_once 'vendor/autoload.php';
session_start();

$client = new Google_Client();
$client->setClientId(clientId: '794050027316-roebaeijkm92f9jlvmrkdgmdos6sc1l1.apps.googleusercontent.com');
$client->setClientSecret(clientSecret: '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');
$client->setRedirectUri(redirectUri: 'http://localhost/slvshop_project/login.php');
$client->addScope(scope_or_scopes: "email");
$client->addScope(scope_or_scopes: "profile");

if (isset($_GET['code'])) {
    $token = $client->fetchAccessTokenWithAuthCode(code: $_GET['code']);

if (isset($token['error'])) {
    // Gagal ambil token
    echo "Error saat mengambil token: " . htmlspecialchars(string: $token['error_description']);
    exit;
}

$client->setAccessToken(token: $token);

    $oauth = new Google_Service_Oauth2(clientOrConfig: $client);
    $userData = $oauth->userinfo->get();

    $_SESSION['user_email'] = $userData->email;
    $_SESSION['user_name'] = $userData->name;
    $_SESSION['user_picture'] = $userData->picture;

    if ($_SESSION['user_email'] === 'kingsan1705@gmail.com') {
        header('Location: admin/admin-dashboard.php');
    } else {
        header(header: 'Location: index2.php');
    }
    exit;
} else {
    $authUrl = $client->createAuthUrl();
    echo "<a href='" . htmlspecialchars(string: $authUrl) . "'>Login dengan Google</a>";
}
?>


