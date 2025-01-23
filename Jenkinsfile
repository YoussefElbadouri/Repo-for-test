pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/YoussefElbadouri/Sbiy3at.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-app .'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv('sonarqube-server') { // Remplacez par le nom configuré dans Jenkins
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        stage('Deploy Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name my-app-container my-app'
            }
        }
    }
}

