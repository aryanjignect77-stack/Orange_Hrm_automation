pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    triggers {
        cron('H 6 * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                    if [ ! -d "${VENV_DIR}" ]; then
                        python3 -m venv ${VENV_DIR}
                    fi
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    . ${VENV_DIR}/bin/activate
                    pytest tests/ \
                        --browser=chrome \
                        --alluredir=reports/allure-results \
                        -v \
                        --tb=short
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports/allure-results']],
                    reportBuildPolicy: 'ALWAYS',
                    report: 'allure-report'
                ])
            }
        }
    }

    post {
        success {
            echo 'All tests passed!'
        }
        failure {
            mail to: 'aryanjignect77@gmail.com',
                 subject: "FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                 body: "Tests failed. Check report: ${env.BUILD_URL}"
        }
        always {
            cleanWs()
        }
    }
}