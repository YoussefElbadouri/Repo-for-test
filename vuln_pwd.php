<?php
$password = "admin123";

// 🚨 Mauvaise pratique : Ne pas hacher le mot de passe avant de le stocker
file_put_contents("passwords.txt", $password); // ❌ Un attaquant peut lire ce fichier
?>
