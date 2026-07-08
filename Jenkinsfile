pipeline {
    agent any

    environment {
        REGISTRY_NAMESPACE = "dit-library"
        IMAGE_TAG          = "${env.BUILD_NUMBER}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Récupération du code depuis GitHub...'
                checkout scm
            }
        }

        stage('Build & Test - book-service') {
            steps {
                dir('book-service') {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --no-cache-dir -r requirements.txt
                        python -m py_compile app/*.py app/routers/*.py
                    '''
                }
            }
        }

        stage('Build & Test - user-service') {
            steps {
                dir('user-service') {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --no-cache-dir -r requirements.txt
                        python -m py_compile app/*.py app/routers/*.py
                    '''
                }
            }
        }

        stage('Build & Test - borrow-service') {
            steps {
                dir('borrow-service') {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --no-cache-dir -r requirements.txt
                        python -m py_compile app/*.py app/routers/*.py
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build -t ${REGISTRY_NAMESPACE}/book-service:${IMAGE_TAG} -t ${REGISTRY_NAMESPACE}/book-service:latest ./book-service
                    docker build -t ${REGISTRY_NAMESPACE}/user-service:${IMAGE_TAG} -t ${REGISTRY_NAMESPACE}/user-service:latest ./user-service
                    docker build -t ${REGISTRY_NAMESPACE}/borrow-service:${IMAGE_TAG} -t ${REGISTRY_NAMESPACE}/borrow-service:latest ./borrow-service
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                    docker compose down --remove-orphans || true
                    docker compose up -d --build
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 15
                    curl -f http://localhost:8001/health
                    curl -f http://localhost:8002/health
                    curl -f http://localhost:8003/health
                '''
            }
        }
    }

    post {
        success { echo 'Pipeline exécuté avec succès.' }
        failure { echo 'Échec du pipeline, voir les logs.' }
        always  { sh 'docker compose ps || true' }
    }
}