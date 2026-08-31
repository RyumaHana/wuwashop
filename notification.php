<?php
require_once 'vendor/autoload.php';
require_once 'koneksi.php';

\Midtrans\Config::$serverKey = 'SB-Mid-server-KIwdsuEh3_CNCxbSMMZMYtw5';
\Midtrans\Config::$isProduction = false;

$notif = new \Midtrans\Notification();
$transaction = $notif->transaction_status;
$order_id = $notif->order_id;

$user_id = $notif->custom_field2;
$server = $notif->custom_field1;
$product = $notif->custom_field3;
$price = $notif->gross_amount;

if ($transaction == 'capture' || $transaction == 'settlement') {
    $stmt = $conn->prepare(query: "INSERT INTO transaksi (user_id, server, product, price) VALUES (?, ?, ?, ?)");
    $stmt->bind_param(types: "sssd", var: $user_id, vars: $server, $product, $price);
    $stmt->execute();
    $stmt->close();
    http_response_code(response_code: 200);
} else {
    http_response_code(response_code: 200);
}
?>
