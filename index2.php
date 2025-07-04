<?php
session_start();
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Solo Leveling: Arise - Top Up</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="style.css" />
    <style>
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap; 
      padding: 10px 20px;
      background-color: white;
      border-bottom: 2px solid #f2f2f2;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .header-left img {
      width: 40px;
      height: auto;
    }

    .header-left h1 {
      font-size: 1.5rem;
      color: #fbc531;
      margin: 0;
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 10px;
    }

    .logout-btn {
      background-color: #fbc531;
      color: #fff;
      font-weight: bold;
      border: none;
      border-radius: 8px;
      padding: 8px 16px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      text-decoration: none;
    }

    .logout-btn:hover {
      background-color: #e1a500;
    }

    /* Responsif untuk layar kecil */
    @media (max-width: 600px) {
      .header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
      }

      .header-left, .header-right {
        flex-direction: column;
        align-items: flex-start;
        width: 100%;
      }

      .header-right {
        align-items: flex-end;
      }

      .logout-btn {
        width: 100%;
        text-align: center;
      }
    }
    </style>

</head>

<body class="bg-purple-50 text-gray-900">
    <header class="flex flex-col sm:flex-row items-center justify-between px-4 py-3 bg-purple-50 shadow-md space-y-2 sm:space-y-0">
  <div class="flex items-center space-x-3">
    <img src="assets/bg/logo.png" alt="Logo" class="h-12 sm:h-14">
    <h1 class="text-2xl sm:text-3xl font-bold text-yellow-500">WUWA SHOP</h1>
  </div>
  <div class="flex items-center space-x-2">
    <?php
    if (isset($_SESSION['user_name'])) {
        echo "<span class='text-sm sm:text-base text-gray-950'>Hello, {$_SESSION['user_name']}</span>";
        echo "<a href='logout.php' class='text-sm sm:text-base text-white font-bold bg-yellow-400 px-4 py-2 rounded hover:bg-yellow-600'>Logout</a>";
    } else {
        require_once 'vendor/autoload.php';
        $client = new Google_Client();
        $client->setClientId('794050027316-roebaeijkm92f9jlvmrkdgmdos6sc1l1.apps.googleusercontent.com');
        $client->setClientSecret('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');
        $client->setRedirectUri('http://localhost/slvshop_project/login.php');
        $client->addScope("email");
        $client->addScope("profile");

        $loginUrl = $client->createAuthUrl();
        echo "<a href='" . htmlspecialchars($loginUrl) . "' class='text-sm sm:text-base text-white font-bold bg-yellow-400 px-4 py-2 rounded hover:bg-yellow-600'>Login</a>";
    }
    ?>
  </div>
</header>


    <div class="top-banner"></div>
    <div class="notice">
        <strong>Silahkan pilih item dibawah, jangan lupa isi server dan UID ya >v<.</strong>
    </div>

    <main class="max-w-3xl mx-auto py-8 px-4 space-y-8">
        <section class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-semibold mb-4">1. Enter User Info</h2>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-1">Select Server</label>
                    <select class="w-full border rounded p-2" id="serverSelect">
            <option value="">-- Choose Server --</option>
            <option value="America">America</option>
            <option value="Asia">Asia</option>
            <option value="Europe">Europe</option>
            <option value="Europe">Europe</option>
            <option value="HMT(HK, MO, TW)">HMT(HK, MO, TW)</option>
            <option value="SEA">SEA</option>
            
          </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Enter User ID</label>
                    <input type="text" id="userId" class="w-full border rounded p-2" placeholder="Enter your UID" />
                </div>
            </div>
        </section>

        <section class="bg-white p-6 rounded-lg shadow">
    <h2 class="text-xl font-semibold mb-4">2. Choose Product</h2>
    <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <?php
        include 'koneksi.php';
        $produk = mysqli_query($conn, "SELECT * FROM produk");
        while ($row = mysqli_fetch_assoc($produk)) {
            $id = $row['id'];
            $nama = $row['nama'];
            $harga = $row['harga'];
            $gambar = "assets/basic_item/" . $row['gambar']; 
        ?>
        <button onclick="selectProduct(<?= $id ?>, '<?= $nama ?>', <?= $harga ?>)" class="product-btn bg-gray-100 hover:bg-indigo-100 p-4 rounded shadow text-center">
            <img src="<?= $row['gambar'] ?>" alt="<?= $row['nama'] ?>" class="w-36 h-36 object-contain">
            <div class="font-semibold"><?= htmlspecialchars($nama) ?></div>
            <div class="text-sm text-gray-500">Rp<?= number_format($harga, 0, ',', '.') ?></div>
        </button>
        <?php } ?>
    </div>
</section>

        <section class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-semibold mb-4">3. Order Summary</h2>
            <p><strong>Server:</strong> <span id="summaryServer">-</span></p>
            <p><strong>User ID:</strong> <span id="summaryUserId">-</span></p>
            <p><strong>Product:</strong> <span id="summaryProduct">-</span></p>
            <p><strong>Total:</strong> Rp<span id="summaryPrice">0.00</span></p>
            <button onclick="checkout()" class="bg-yellow-400 font-bold text-zinc-950 px-4 py-2 rounded hover:bg-yellow-600">Buy Now</button>
        </section>
    </main>

    <script>
        let selectedProduct = null;

        function selectProduct(id, name, price) {
            selectedProduct = {
                id,
                name,
                price
            };
            document.getElementById('summaryProduct').textContent = name;
            document.getElementById('summaryPrice').textContent = price.toFixed(2);
        }

        function checkout() {
            const server = document.getElementById('serverSelect').value;
            const userId = document.getElementById('userId').value;
            document.getElementById('summaryServer').textContent = server;
            document.getElementById('summaryUserId').textContent = userId;

            if (!server || !userId || !selectedProduct) {
                alert('Please complete all steps before checkout.');
                return;
            }
            const url = `konfirmasi.php?user_id=${encodeURIComponent(userId)}&server=${server}&product=${encodeURIComponent(selectedProduct.name)}&price=${selectedProduct.price}`;
            window.location.href = url;
        }
    </script>
<footer>
    <p class="store-text">© 2020 WUWAshop Service. All rights reserved.</p>
</footer>
</body>

</html>