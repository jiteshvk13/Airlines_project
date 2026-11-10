pipeline {
    agent any
    
    environment {
        VENV_DIR = 'venv'
        DOCKERHUB_CREDENTIAL_ID = 'mlops-airlines'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'jiteshvk13/mlops-airlines'
    }
    
    stages {
        stage('Cloning From Github Repo') {
            steps {
                script {
                    echo 'Cloning From Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-token', url: 'https://github.com/jiteshvk13/Airlines_project.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setup Virtual Environment...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Code Linting') {
            steps {
                script {
                    echo 'Code Linting...'
                    sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    pylint application.py main.py --output=pylint-report.txt --exit-zero || echo "Pylint Stage Completed"
                    flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt  || echo "Flake8 Stage Completed"
                    black application.py main.py || echo "black Stage Completed"
                    '''
                }
            }
        }

        stage('Trivy Scaning') {
            steps {
                script {
                    echo 'Trivy Scaning...'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }

        stage('Building Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

         stage('Scanning Docker Image') {
            steps {
                script {
                    echo 'Scanning Docker Image...'
                    sh "trivy image --timeout 15m ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-scan-report.txt"
                }
            }
        }
        stage('Pushing Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker Image...'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}"){
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}