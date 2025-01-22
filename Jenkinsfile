pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/YoussefElbadouri/Sbiy3at.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t my-app .'
            }
        }
        stage('Static Analysis with SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }
        stage('Test') {
            steps {
                echo 'No tests implemented yet.'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 5000:5000 my-app'
            }
        }
    }
}
