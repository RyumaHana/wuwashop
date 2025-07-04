<?php
$host = 'localhost';
$db = 'slvshop_db';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO(dsn: "mysql:host=$host;dbname=$db", username: $user, password: $pass);
    $pdo->setAttribute(attribute: PDO::ATTR_ERRMODE, value: PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("DB Connection failed: " . $e->getMessage());
}
?>