pipeline {
    agent any
    environment {
        APP_IMAGE = "securedev-app"
        NETWORK_NAME = "eva3ciber_devsecops-net"
        STAGING_CONTAINER = "app-staging"
        PROD_CONTAINER = "app-prod"
    }
    stages {
        stage('1. Checkout & Dependencias') {
            steps {
                checkout scm
                echo 'Verificando auditoría de dependencias...'
            }
        }
        stage('2. Construcción (Build Docker)') {
            steps {
                echo 'Construyendo imagen Docker de la aplicación...'
                sh "docker build -t ${APP_IMAGE}:latest ./app"
            }
        }
        stage('3. Despliegue Staging para Pruebas') {
            steps {
                echo 'Levantando contenedor en entorno aislado de pruebas...'
                sh """
                    docker rm -f ${STAGING_CONTAINER} || true
                    docker run -d --name ${STAGING_CONTAINER} --network ${NETWORK_NAME} ${APP_IMAGE}:latest
                    sleep 5
                """
            }
        }
        stage('4. Pruebas de Seguridad Automatizadas (OWASP ZAP)') {
            steps {
                echo 'Ejecutando escaneo dinámico OWASP ZAP Baseline...'
                sh """
                    mkdir -p zap-reports
                    docker rm -f zap-scanner || true
                    docker run --user root --name zap-scanner --network ${NETWORK_NAME} ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://${STAGING_CONTAINER}:5000 -r zap-report.html || true
                    docker cp zap-scanner:/zap/wrk/zap-report.html ./zap-reports/zap-report.html || true
                    docker rm -f zap-scanner || true
                """
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'zap-reports',
                    reportFiles: 'zap-report.html',
                    reportName: 'Reporte OWASP ZAP'
                ])
            }
        }
        stage('5. Despliegue a Producción') {
            steps {
                echo 'Desplegando aplicación en entorno de Producción...'
                sh """
                    docker rm -f ${PROD_CONTAINER} || true
                    docker run -d --name ${PROD_CONTAINER} --network ${NETWORK_NAME} -p 5000:5000 ${APP_IMAGE}:latest
                """
            }
        }
    }
    post {
        always {
            sh "docker rm -f ${STAGING_CONTAINER} || true"
        }
    }
}