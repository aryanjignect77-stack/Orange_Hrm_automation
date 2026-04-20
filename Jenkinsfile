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
                    if not exist "%VENV_DIR%" (
                        python -m venv %VENV_DIR%
                    )
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat '''
                        call %VENV_DIR%\\Scripts\\activate.bat
                        pytest tests/ --browser=chrome --alluredir=reports/allure-results -v --tb=short
                    '''
                }
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