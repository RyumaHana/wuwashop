<?php
// midtrans_proses.php

require_once 'vendor/autoload.php'; // pastikan composer sudah di-install

// Konfigurasi Midtrans
\Midtrans\Config::$serverKey = 'SB-Mid-server-KIwdsuEh3_CNCxbSMMZMYtw5';
\Midtrans\Config::$isProduction = false;
\Midtrans\Config::$isSanitized = true;
\Midtrans\Config::$is3ds = true;

// Ambil data dari form
$server  = $_POST['server'];
$product = $_POST['product'];
$price   = (int) $_POST['price'];
$order_id = rand(); // ID unik

// Data transaksi ke Midtrans
$params = [
    'transaction_details' => [
        'order_id' => $order_id,
        'gross_amount' => $price,
    ],
    'customer_details' => [
        'first_name' => $server,
        'email' => 'dummy@example.com', // opsional, bisa diganti jika ada email input
    ],
    'item_details' => [
        [
            'id' => $product,
            'price' => $price,
            'quantity' => 1,
            'name' => $product
        ]
    ]
];

// Buat Snap Token
$snapToken = \Midtrans\Snap::getSnapToken($params);
?>

<!DOCTYPE html>
<html>
<head>
    <title>Pilih Metode Pembayaran</title>
    <script src="https://app.sandbox.midtrans.com/snap/snap.js" data-client-key="SB-Mid-client-Gn_uWT500mMAjBP0"></script>
    <style>
    body {
      background: linear-gradient(to right, #e0e7ff, #fef9ff);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100vh;
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
  </style>
</head>
<body>
    <h3>Server: <?= htmlspecialchars($server) ?>, Produk: <?= htmlspecialchars($product) ?>, Harga: Rp <?= number_format($price, 0, ',', '.') ?></h3>
    <button id="pay-button">Pilih Metode Pembayaran</button>

    <script type="text/javascript">
        document.getElementById('pay-button').addEventListener('click', function () {
            snap.pay('<?= $snapToken ?>');
        });
    </script>
</body>
</html>
