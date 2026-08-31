<?php
session_start();
if (!isset($_SESSION['user_email'])) {
    header(header: "Location: login.php");
    exit;
}

$user_email = $_SESSION['user_email'];
$server = $_GET['server'] ?? '';
$user_id = $_GET['user_id'] ?? '';
$product = $_GET['product'] ?? '';
$price = $_GET['price'] ?? '';

if (!$server || !$user_id || !$product || !$price) {
    echo "Data tidak lengkap.";
    exit;
}

// Koneksi ke database (XAMPP - MySQL)
$host = 'localhost';
$db = 'slvshop_db';
$user = 'root';
$pass = '';

$conn = new mysqli(hostname: $host, username: $user, password: $pass, database: $db);
if ($conn->connect_error) {
    die("Koneksi gagal: " . $conn->connect_error);
}

// Simpan transaksi ke database
$stmt = $conn->prepare("INSERT INTO transaksi (email, server, user_id, produk, harga, status) VALUES (?, ?, ?, ?, ?, 'pending')");
$stmt->bind_param("ssssd", $user_email, $server, $user_id, $product, $price);
$stmt->execute();
$stmt->close();
$conn->close();

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Konfirmasi Pembelian</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
    body {
      background: linear-gradient(to right, #e0e7ff, #fef9ff);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 80vh;
      margin: 0;
      color: #1f2937;
    }

    .container {
      background-color: white;
      padding: 32px;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
      text-align: center;
      max-width: 500px;
      width: 90%;
    }

    h3 {
      font-size: 1.125rem;
      margin-bottom: 24px;
    }

    #pay-button {
      background-color: #4f46e5;
      color: white;
      padding: 12px 24px;
      font-size: 1rem;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.2s ease;
    }

    #pay-button:hover {
      background-color: #4338ca;
      transform: scale(1.05);
    }

    footer {
      background-color:rgb(255, 214, 32);
      color:rgb(43, 43, 43);
      font-weight: bold;
      border-radius: 20px;
      text-align: center;
      padding: 10px 20px;
      margin-top: 20px;
    }
  </style>
</head>
<body class="bg-gray-100 text-gray-900">
    <div class=" mt-12 bg-purple-50 p-6 rounded shadow text-center">
        <h1 class="text-xl font-bold mb-4">Konfirmasi Pembelian</h1>
        <p><strong>Email:</strong> <?= htmlspecialchars(string: $user_email) ?></p>
        <p><strong>Server:</strong> <?= htmlspecialchars(string: $server) ?></p>
        <p><strong>User ID:</strong> <?= htmlspecialchars(string: $user_id) ?></p>
        <p><strong>Produk:</strong> <?= htmlspecialchars(string: $product) ?></p>
        <p><strong>Harga:</strong> $<?= htmlspecialchars(string: $price) ?></p>

        <p class="mt-4 text-yellow-600 font-semibold">Sedang diproses...</p>

        <!-- Simulasi tombol bayar otomatis -->
        <form action="midtrans_proses.php" method="POST" class="mt-6">
            <input type="hidden" name="user_email" value="<?= htmlspecialchars(string: $user_email) ?>">
            <input type="hidden" name="user_id" value="<?= htmlspecialchars(string: $user_id) ?>">
            <input type="hidden" name="server" value="<?= htmlspecialchars(string: $server) ?>">
            <input type="hidden" name="product" value="<?= htmlspecialchars(string: $product) ?>">
            <input type="hidden" name="price" value="<?= htmlspecialchars(string: $price) ?>">
            <button type="submit" class="bg-yellow-400 font-bold text-zinc-950 px-4 py-2 rounded hover:bg-yellow-600">Bayar Sekarang</button>
        </form>
    </div>
    <footer>
    <p class="store-text">TERIMAKASIH, SILAHKAN KLIK "BAYAR SEKARANG".</p>
</footer>
</body>
</html>
