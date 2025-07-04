<?php
session_start();
if (!isset($_SESSION['user_email'])) {
    header(header: 'Location: login.php');
    exit;
}
include 'db.php'; 

$email = $_SESSION['user_email'];
$query = $conn->prepare(query: "SELECT * FROM purchases WHERE user_email = ? ORDER BY purchase_time DESC");
$query->bind_param(types: "s", var: $email);
$query->execute();
$result = $query->get_result();

echo "<h2>Riwayat Pembelian</h2><ul>";
while ($row = $result->fetch_assoc()) {
    echo "<li>{$row['product_name']} - \${$row['price']} - {$row['purchase_time']}</li>";
}
echo "</ul>";
