<?php
$host = "localhost";
$user = "root";
$pass = "";
$db = "slvshop_db";

$conn = new mysqli(hostname: $host, username: $user, password: $pass, database: $db);
if ($conn->connect_error) {
    die("Koneksi gagal: " . $conn->connect_error);
}
?>
