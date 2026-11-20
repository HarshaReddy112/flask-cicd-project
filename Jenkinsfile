
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        DEPLOY_DIR = "${WORKSPACE}/deployment"
        APP_PORT = "5001"
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
                sh '''
                    venv/bin/pytest -v test_app.py
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    mkdir -p "$DEPLOY_DIR"

                    cp app.py requirements.txt "$DEPLOY_DIR/"

                    if [ -f "$DEPLOY_DIR/app.pid" ]; then
                        kill "$(cat "$DEPLOY_DIR/app.pid")" 2>/dev/null || true
                    fi

                    nohup "$WORKSPACE/venv/bin/python" \
                    "$DEPLOY_DIR/app.py" \
                    > "$DEPLOY_DIR/app.log" 2>&1 &

                    echo $! > "$DEPLOY_DIR/app.pid"

                    sleep 3
                '''
            }
        }

        stage('Post Deployment Verification') {
            steps {
                sh '''
                    RESPONSE=$(curl -s -w "\\n%{http_code}" \
                    http://127.0.0.1:$APP_PORT/)

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
            echo 'CI/CD Pipeline failed. Check the console output.'
        }
    }
}

