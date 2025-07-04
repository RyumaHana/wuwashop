<?php
session_start();
session_destroy();
header(header: "Location: index2.php");
exit;
?>
