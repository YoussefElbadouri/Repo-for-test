#!/bin/bash
set -euxo pipefail

# Variables
SONAR_SCANNER_VERSION="5.0.1.3006"
ZAP_VERSION="2.16.0"

# Mettre à jour les paquets
sudo apt update && sudo apt upgrade -y

# Installer les dépendances nécessaires
sudo apt install -y openjdk-17-jdk curl unzip docker.io git

# Configurer Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
sudo chmod 777 /var/run/docker.sock

# Exécuter SonarQube
docker run -d --name sonarqube -p 9000:9000 sonarqube

# Installer Sonar Scanner
curl -O "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip"
unzip "sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip"
sudo mv "sonar-scanner-${SONAR_SCANNER_VERSION}-linux" /opt/sonar-scanner
echo 'export PATH=$PATH:/opt/sonar-scanner/bin' >> ~/.bashrc
source ~/.bashrc

# Vérifier Sonar Scanner
sonar-scanner --version || echo "Sonar Scanner installé"

# Installer Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins -y
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Télécharger et configurer OWASP ZAP
wget "https://github.com/zaproxy/zaproxy/releases/download/v${ZAP_VERSION}/ZAP_${ZAP_VERSION}_Linux.tar.gz"
tar -xvzf "ZAP_${ZAP_VERSION}_Linux.tar.gz"
cd "ZAP_${ZAP_VERSION}"
nohup ./zap.sh -daemon -host 0.0.0.0 -port 9090 -config api.key=your_api_key > ~/zap.log 2>&1 &

# Message de fin
echo "Configuration terminée avec succès !"
