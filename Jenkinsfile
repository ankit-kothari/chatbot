def NAME = 'chatbot'
def TAG    = 'git log -1 --pretty=%!H(MISSING))'
def IMG   = ${NAME}:${TAG}
def LATEST  = ${NAME}:'latest'
pipeline
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
               sh 'docker build image -t ${IMG} .'
               sh 'docker tag ${IMG} ${LATEST}'
        }
    }
    stage('Run Image') {
           steps {
               sh 'docker run ${LATEST} '
        }
    }
