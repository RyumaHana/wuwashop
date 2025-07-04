<?php
require_once 'vendor/autoload.php';
require_once 'db.php';

\Midtrans\Config::$serverKey = 'SB-Mid-server-KIwdsuEh3_CNCxbSMMZMYtw5';
\Midtrans\Config::$isProduction = false;
\Midtrans\Config::$isSanitized = true;
\Midtrans\Config::$is3ds = true;

$user_id = $_GET['user_id'];
$server = $_GET['server'];
$product = $_GET['product'];
$price = $_GET['price'];
$email = $_SESSION['user_email'];
$name = $_SESSION['user_name'];

$order_id = 'SLV-' . time();

$stmt = $pdo->prepare(query: "INSERT INTO transactions (user_email, user_name, server, user_id, product_name, price, status) VALUES (?, ?, ?, ?, ?, ?, 'pending')");
$stmt->execute(params: [$email, $name, $server, $user_id, $product, $price]);

$params = [
  'transaction_details' => [
    'order_id' => $order_id,
    'gross_amount' => (int)$price
  ],
  'customer_details' => [
    'first_name' => $name,
    'email' => $email
  ]
];

$snapToken = \Midtrans\Snap::getSnapToken(params: $params);
?>

<script src="https://app.sandbox.midtrans.com/snap/snap.js" data-client-key="SB-Mid-client-Gn_uWT500mMAjBP0"></script>
<script>
  snap.pay("<?= $snapToken ?>", {
    onSuccess: function(result) {
      alert("Pembayaran sukses!");
      window.location.href = 'history.php';
    },
    onPending: function(result) {
      alert("Menunggu pembayaran...");
    },
    onError: function(result) {
      alert("Pembayaran gagal.");
    }
  });
</script>
