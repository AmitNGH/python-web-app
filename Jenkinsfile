pipeline {
    agent any

    environment {
        // Set up environment variables if needed
        WEBAPP_DIR= 'webapp'
        VENV_DIR = 'venv'
        DB_CONTAINER = "python-web-app-mysql-1"

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
                    sh 'docker compose up -d'
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
//
//         stage('Test') {
//             steps {
//                 script {
// //                     sh 'docker network connect jenkins ${DB_CONTAINER}'
// //                     ip = sh(script: 'docker inspect -f "{{.NetworkSettings.Networks.jenkins.IPAddress}}" ${CONTAINER_NAME}', returnStdout: true).trim()
// //                     echo "IP Address: ${ip}"
//
//                     sh """
//                         . ./${VENV_DIR}/bin/activate
//                         ./${VENV_DIR}/bin/python ./WorldOfGames/e2e.py "${ip}" "${PORT}"
//                     """
//                 }
//             }
//         }

        stage("Run Backend Tests") {
            steps {
                sh """
                    . ./${VENV_DIR}/bin/activate
                    ./${VENV_DIR}/bin/python ${WEBAPP_DIR}/test/backend_testing.py
                """
//                 sh 'ls -l ${WEBAPP_DIR}'
//                 sh '. ${WEBAPP_DIR}/${VENV_DIR}/bin/activate'
//                 sh 'python3 ${WEBAPP_DIR}/test/backend_testing.py'
            }
        }

//         stage("Run Frontend Tests") {
//             steps {
//
//             }
//         }
//
//         stage("Run Combined Tests") {
//             steps {
//
//             }
//         }
//
//         stage("Clean Environment") {
//             steps {
//
//             }
//         }
    }

    post {
        always {
            // Clean up the workspace
            script {
                sh """
                    . ./${VENV_DIR}/bin/activate
                    ./${VENV_DIR}/bin/python ${WEBAPP_DIR}/clean_environment.py
                """
                sh 'docker compose down -d'
                sh 'rm -r db'
            }
        }
        success {
            // Actions to take on success
            echo 'Pipeline succeeded'
        }
        failure {
            // Actions to take on failure
            echo 'Pipeline failed'
        }
    }
}