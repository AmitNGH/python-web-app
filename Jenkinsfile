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
                    docker volume rm db
                    sh 'docker compose up -d'
                    sh 'sleep 30'
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
                    sh "cat ${WEBAPP_DIR}/config.ini"


                    withCredentials([usernamePassword(credentialsId: 'db-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                        def frontend_query = "UPDATE config SET endpoint_url = \\\"${ip}\\\" WHERE endpoint_name = 'frontend';"
                        def backend_query = "UPDATE config SET endpoint_url = \\\"${ip}\\\" WHERE endpoint_name = 'backend';"

                        // Run the query using mysql command
                        sh """
                            mysql -h ${ip} -u ${DB_USER} --password=${DB_PASS} ${DB_NAME} -e "${frontend_query}"
                            mysql -h ${ip} -u ${DB_USER} --password=${DB_PASS} ${DB_NAME} -e "${backend_query}"
                        """

                        // jdbc('db') {
                        //     sql("UPDATE config SET endpoint_url = ${ip} WHERE endpoint_name = 'frontend';")
                        //     sql("UPDATE config SET endpoint_url = ${ip} WHERE endpoint_name = 'backend';")
                        // }
                    }

                    sh """
                        . ./${VENV_DIR}/bin/activate
                        ./${VENV_DIR}/bin/python ./WorldOfGames/e2e.py "${ip}" "${DB_PORT}"
                    """
                }
            }
        }

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
            script {
                // sh """
                //     . ./${VENV_DIR}/bin/activate
                //     ./${VENV_DIR}/bin/python ${WEBAPP_DIR}/clean_environment.py
                // """
                sh 'docker logs ${DB_CONTAINER}'
                // sh 'docker compose down'
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