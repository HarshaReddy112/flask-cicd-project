

pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        APP_PORT = "5001"
        APP_NAME = "flask-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                sh 'venv/bin/pytest -v test_app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t flask-app .
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker rm -f $APP_NAME 2>/dev/null || true

                    docker run -d \
                        --name $APP_NAME \
                        -p 5001:5001 \
                        flask-app
                '''
            }
        }

        stage('Post Deployment Verification') {
            steps {
                sh '''
                    for i in $(seq 1 15); do
                        if curl -fsS http://127.0.0.1:5001/; then
                            break
                        fi
                        sleep 2
                    done

                    RESPONSE=$(curl -s -w "\\n%{http_code}" \
                        http://127.0.0.1:5001/)

                    echo "$RESPONSE"

                    echo "$RESPONSE" | grep -q \
                        "Welcome to Flask CI/CD Pipeline!"

                    echo "$RESPONSE" | grep -q "200"
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed!'
        }
    }
}
