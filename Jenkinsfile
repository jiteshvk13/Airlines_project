pipeline {
    agent any
    
    stages {
        stage('Cloning From Github Repo') {
            steps {
                script {
                    echo 'Cloning From Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-token', url: 'https://github.com/jiteshvk13/Airlines_project.git']])
                }
            }
        }
    }
}