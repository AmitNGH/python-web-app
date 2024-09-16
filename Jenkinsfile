pipeline {
    agent any

    environment {
        // Set up environment variables if needed
        WEBAPP_DIR= 'webapp'
        VENV_DIR = 'venv'

    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'second-part', url: 'https://github.com/AmitNGH/python-web-app'
            }
        }

        stage('Setup Python Environment') {
            steps {
                // // Set up a virtual environment
                sh 'python3 -m venv ${WEBAPP_DIR}/${VENV_DIR}'
                sh '. ${WEBAPP_DIR}/${VENV_DIR}/bin/activate'

                // Upgrade pip and install dependencies
                sh '${WEBAPP_DIR}/${VENV_DIR}/bin/pip install --upgrade pip'
                sh '${WEBAPP_DIR}/${VENV_DIR}/bin/pip install -r ${WEBAPP_DIR}/requirements.txt'

                // sh 'pip install --upgrade pip'
                // sh 'pip install -r requirements.txt'
            }
        }

        stage("Run Backend Tests") {
            steps {
                sh 'ls -l ${WEBAPP_DIR}'
                sh '. ${WEBAPP_DIR}/${VENV_DIR}/bin/activate'
                sh 'python3 ${WEBAPP_DIR}/test/backend_testing.py'
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
            sh 'python3 ${WEBAPP_DIR}/clean_environment.py'
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