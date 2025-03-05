<?php
// 🚨 Mauvaise pratique : Afficher une entrée utilisateur sans la filtrer
$user_input = $_GET['name'];  
echo "Hello, " . $user_input; // ❌ XSS possible si l'utilisateur insère <script>alert('XSS')</script>
?>
