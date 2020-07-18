pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Built Successfully'
      }
    }

    stage('run') {
      steps {
        sh 'python pytest Tests.py'
      }
    }

  }
}