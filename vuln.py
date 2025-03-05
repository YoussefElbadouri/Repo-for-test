import os

# 🚨 Mauvaise pratique : exécuter une commande système avec des entrées non filtrées
command = input("Enter command: ")
os.system(command)  # ❌ Injection de commande possible !
