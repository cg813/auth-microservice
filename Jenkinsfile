def gv
pipeline{
    agent { label 'master' }
    environment {
        SERVER_CREDENTIALS = credentials('jenkins-gcr-account')
    }
    stages{
        stage("Load script") {
            steps {
                script {
                    gv = load "script.groovy"
                    env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT} | head -n1', returnStdout: true).stripIndent().trim()
                    env.GIT_AUTHOR = sh (script: 'git log -1 --pretty=%ae ${GIT_COMMIT} | awk -F "@" \'{print $1}\' | grep -Po "[a-z]{1,}" | head -n1', returnStdout: true).trim()

                }
            }
        }
        stage("Build Image") {
            when {
                branch 'master'
            }
            agent { label "builder" }
            steps {
              slackSend (color: '#00FF00', message: "build - ${env.BUILD_NUMBER} ${env.JOB_NAME} Started  ${env.BUILD_NUMBER}  by changes from ${env.GIT_AUTHOR} commit message ${env.GIT_COMMIT_MSG} (<${env.BUILD_URL}|Open>)")
                script {
                    gv.buildImage()
                }
            }
        }
        stage("Backend test") {
            when {
                not {
                    anyOf {
                        branch 'master'
                    }
                }
            }
            agent { label "builder" }
            steps {
              slackSend (color: '#00FF00', message: "Unit Test  - ${env.BUILD_NUMBER} ${env.JOB_NAME} Started  ${env.BUILD_NUMBER} for user: ${env.GIT_AUTHOR} commit message ${env.GIT_COMMIT_MSG} (<${env.BUILD_URL}|Open>)")
                script {
                    gv.TestApp()
                }
            }
        }
        stage("Push tested image to Repo") {
            when {
                branch 'master'
            }
            agent { label "builder" }
            steps {
              slackSend (color: '#00FF00', message: "Push tested ${env.BRANCH_NAME} image to repo No - ${env.BUILD_NUMBER} ${env.JOB_NAME} Started ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
                script {
                    gv.PushImage()
                }
            }
        }
        stage('Approval') {
            // no agent, so executors are not used up when waiting for approvals
            agent none
            steps {
                script {
                    def deploymentDelay = input id: 'Deploy', message: 'Deploy to production?', submitter: 'rkivisto,admin', parameters: [choice(choices: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'], description: 'Hours to delay deployment?', name: 'deploymentDelay')]
                    sleep time: deploymentDelay.toInteger(), unit: 'HOURS'
                }
            }
        }
        stage('Deploy') {
            steps {
                lock(resource: 'deployApplication'){
                    echo 'Deploying...'
                    script{
                        gv.DeployToDev()
                    }
                }
            }
        }
    }  
    post {
    success {
      slackSend (color: '#00FF00', message: "Success  job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.BUILD_URL}|Open>)")
    }
    failure {
      slackSend (color: '#FF0000', message: "Failed: job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.BUILD_URL}|Open>)")
    }
  }
}
