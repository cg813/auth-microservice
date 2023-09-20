
def buildImage() {
    echo "Starting application build"
    withCredentials([file(credentialsId: 'jenkins-gcr-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        sh 'docker login -u _json_key -p "`cat ${GOOGLE_APPLICATION_CREDENTIALS}`" https://gcr.io'
        sh 'docker build -f auth/Dockerfile.prod auth -t auth-service'
        sh 'docker tag auth-service gcr.io/mima-325516/authentication'
    }
    echo "Image pushed to GCP"
}

def PushImage() {
    echo "Push Tested image to repo"
    withCredentials([file(credentialsId: 'jenkins-gcr-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        sh 'docker login -u _json_key -p "`cat ${GOOGLE_APPLICATION_CREDENTIALS}`" https://gcr.io'
        sh 'docker tag gcr.io/mima-325516/authentication gcr.io/mima-325516/authentication:dev'
        sh 'docker tag gcr.io/mima-325516/authentication gcr.io/mima-325516/authentication:prod'
        sh 'docker push gcr.io/mima-325516/authentication:dev'
        sh 'docker push gcr.io/mima-325516/authentication:prod'

    }
    echo "Image pushed to Google container registry"
}

def TestApp() {
    echo "Starting unit test"
    sh 'docker network create mima_network && docker-compose -f docker-compose.test.yml up -d && docker-compose -f auth/docker-compose.yml exec auth-srv pytest -s -v && docker-compose -f docker-compose.test.yml down && docker network rm mima_network'
}

def DeployToDev() {
    sh 'echo "starting deployment"'
    sh 'cd /opt/configuration/charts/ && /usr/local/bin/helm upgrade \
    --install  --wait --atomic authenticate auth-service \
    --values /opt/configuration/dev/values-auth-service.yaml \
    --set image.releaseDate=VRSN`date +%Y%m%d-%H%M%S` --set image.tag=dev \
    -n dev'
    echo "Core app deployed to dev env"
}

def DeployToProd() {
    sh 'echo "starting deployment "'
    sh 'cd /opt/configuration/charts/'
    sh 'cd /opt/configuration/charts/ && /usr/local/bin/helm upgrade \
    --install  --wait --atomic authenticate auth-service \
    --values /opt/configuration/prod/values-auth-service.yaml \
    --set image.releaseDate=VRSN`date +%Y%m%d-%H%M%S` --set image.tag=prod \
    -n prod'
    echo "Core app deployed to prod"
}

return this
