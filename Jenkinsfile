pipeline {
    agent any

    environment {
        SPARK_HOME = '/home/hr295/spark'
        SPARK_FILE_PATH = '/home/hr295/spark_files/read_and_write_to_psql1.py'
        SPARK_SERVER = '192.168.1.77' // Remote server IP
    }

    stages {
        stage('Run Spark Job on Remote Server') {
            steps {
                script {
                    // Using SSH to submit the Spark job remotely
                    sshagent(['spark-server-ssh-credential-id']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no hr295@${SPARK_SERVER} << 'EOF'
                        set -e  # Exit immediately if a command fails
                        echo "Starting Spark job on remote server..."
                        ${SPARK_HOME}/bin/spark-submit \\
                            --master local[*] \\
                            --driver-memory 4g \\
                            --executor-memory 4g \\
                            ${SPARK_FILE_PATH}
                        echo "Spark job completed successfully."
                        EOF
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Spark job executed successfully on remote server."
        }
        failure {
            echo "Failed to execute Spark job on remote server."
        }
    }
}


