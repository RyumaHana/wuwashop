<?php
require_once 'vendor/autoload.php';

\Midtrans\Config::$serverKey = 'SB-Mid-server-KIwdsuEh3_CNCxbSMMZMYtw5';
\Midtrans\Config::$isProduction = false;
\Midtrans\Config::$isSanitized = true;
\Midtrans\Config::$is3ds = true;

$params = array(
  'transaction_details' => array(
    'order_id' => rand(),
    'gross_amount' => $_GET['price'],
  ),
  'customer_details' => array(
    'email' => $_SESSION['user_email'],
    'first_name' => $_SESSION['user_name'],
  )
);

$snapToken = \Midtrans\Snap::getSnapToken(params: $params);
?>

<script src="https://app.sandbox.midtrans.com/snap/snap.js" data-client-key="SB-Mid-client-Gn_uWT500mMAjBP0"></script>
<button onclick="pay()">Bayar Sekarang</button>

<script>
function pay() {
  snap.pay("<?= $snapToken ?>", {
    onSuccess: function(result){ console.log("Sukses", result); },
    onPending: function(result){ console.log("Pending", result); },
    onError: function(result){ console.log("Gagal", result); }
  });
}
</script>
