pipeline {
    agent any
    environment {
        DOCKERHUB_USER = "your-dockerhub-username"
        IMAGE_NAME = "flask-devops-app"
    }
    stages {
        stage('Clone Repo') {
            steps { git 'https://github.com/your-username/devops-flask-project.git' }
        }
        stage('Build Docker Image') {
            steps { sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:latest ." }
        }
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/deployment.yaml"
                sh "kubectl apply -f k8s/service.yaml"
            }
        }
    }
}