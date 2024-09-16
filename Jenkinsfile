pipeline {
    agent any

    environment {
        // Set up environment variables if needed
        WEBAPP_DIR= 'webapp'
        VENV_DIR = 'venv'
        DB_CONTAINER = "python-web-app-mysql-1"
        PYTHONPATH = './webapp'
        DB_PORT = 3306
        DB_NAME = 'db'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'second-part', url: 'https://github.com/AmitNGH/python-web-app'
            }
        }

        stage('Start DB') {
            steps {
                script {
                    sh 'docker compose down -v'
                    sh 'docker compose up --build -d'
                    sh 'sleep 10'
                }
            }
        }


        stage('Setup Python Environment') {
            steps {
                // // Set up a virtual environment
                sh """
                    python3 -m venv ./${VENV_DIR}
                    . ./${VENV_DIR}/bin/activate
                    ./${VENV_DIR}/bin/pip install -r ./${WEBAPP_DIR}/requirements.txt
                    ./${VENV_DIR}/bin/pip install requests
                """
            }
        }

        stage('Setup Tests') {
            steps {
                script {
                    sh 'docker network connect jenkins ${DB_CONTAINER}'
                    ip = sh(script: 'docker inspect -f "{{.NetworkSettings.Networks.jenkins.IPAddress}}" ${DB_CONTAINER}', returnStdout: true).trim()
                    sh "sed -i 's/^host=.*/host=${ip}/' ${WEBAPP_DIR}/config.ini"


                    withCredentials([usernamePassword(credentialsId: 'db-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                        def frontend_query = "UPDATE config SET endpoint_url = \\\"127.0.0.1\\\" WHERE endpoint_name = 'frontend';"
                        def backend_query = "UPDATE config SET endpoint_url = \\\"127.0.0.1\\\" WHERE endpoint_name = 'backend';"

                        // Run the query using mysql command
                        sh """
                            mysql -h ${ip} -u ${DB_USER} --password=${DB_PASS} ${DB_NAME} -e "${frontend_query}"
                            mysql -h ${ip} -u ${DB_USER} --password=${DB_PASS} ${DB_NAME} -e "${backend_query}"
                        """
                    }
                }
            }
        }

        stage("Run Backend Tests") {
            steps {
                sh """
                    . ./${VENV_DIR}/bin/activate
                    ./${VENV_DIR}/bin/python ${WEBAPP_DIR}/test/backend_testing.py
                """
            }
        }

        stage("Run Frontend Tests") {
            steps {
                sh """
                    . ./${VENV_DIR}/bin/activate
                    ./${VENV_DIR}/bin/python ${WEBAPP_DIR}/test/frontend_testing.py
                """
            }
        }

        stage("Run Combined Tests") {
            steps {
                sh """
                    . ./${VENV_DIR}/bin/activate
                    ./${VENV_DIR}/bin/python ${WEBAPP_DIR}/test/combined_testing.py
                """
            }
        }
    }

    post {
        always {
            script {
                sh 'docker compose down'
            }
        }
    }
}