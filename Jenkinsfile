pipeline {
  agent any
    stages {
       stage('CLone Repository') {
       /* CLoning the repository to our workspac */
         steps {
               checkout scm
       }
    }
        stage('Build Image') {
           steps {
               sh 'docker build -t chatbot:v1 .'
        }
    }
    stage('Run Image') {
           steps {
               sh 'docker run -d chatbot:v1'
        }
    }
    }
}
