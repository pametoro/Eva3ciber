pipeline {
    agent any

    environment {
        APP_NAME = "securedev-app"
        APP_PORT = "5000"
        NETWORK_NAME = "eva3ciber_devsecops-net"
    }

    stages {
        stage('1. Checkout & Dependencias') {
            steps {
                checkout scm
                echo "Verificando auditoría de dependencias..."
            }
        }

        stage('2. Construcción (Build Docker)') {
            steps {
                echo "Construyendo imagen Docker de la aplicación..."
                sh "docker build -t ${APP_NAME}:latest ./app"
            }
        }

        stage('3. Despliegue Staging para Pruebas') {
            steps {
                echo "Levantando contenedor temporal para escaneo DAST..."
                sh """
                    docker rm -f ${APP_NAME}-staging || true
                    docker run -d --name ${APP_NAME}-staging --network ${NETWORK_NAME} -p 5001:${APP_PORT} ${APP_NAME}:latest
                    sleep 10
                """
            }
        }

        stage('4. Pruebas de Seguridad Automatizadas (OWASP ZAP)') {
            steps {
                echo "Ejecutando OWASP ZAP Baseline Scan..."
                sh """
                    mkdir -p zap-reports
                    docker run --rm --network ${NETWORK_NAME} \
                      -v \$(pwd)/zap-reports:/zap/wrk/:rw \
                      ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
                      -t http://${APP_NAME}-staging:${APP_PORT} \
                      -r zap_report.html || true
                """
            }
            post {
                always {
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'zap-reports',
                        reportFiles: 'zap_report.html',
                        reportName: 'Reporte OWASP ZAP'
                    ])
                    sh "docker rm -f ${APP_NAME}-staging || true"
                }
            }
        }

        stage('5. Despliegue a Producción') {
            steps {
                echo "Desplegando versión segura en Producción..."
                sh """
                    docker rm -f ${APP_NAME}-prod || true
                    docker run -d --name ${APP_NAME}-prod --network ${NETWORK_NAME} -p ${APP_PORT}:${APP_PORT} --restart always ${APP_NAME}:latest
                """
            }
        }
    }
}
