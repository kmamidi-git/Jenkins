pipeline {
    agent any

    environment {
        SPARK_HOME = '/home/hr295/spark'
        SPARK_SCRIPT_PATH = '/home/hr295/spark_files/read_and_write_to_psql1.py' 
        SPARK_SERVER = '192.168.1.77'
        JDBC_JAR_PATH = '/home/hr295/spark/jars/postgresql-42.6.0.jar'
    }

    stages {
        stage('Run Spark Job on Remote Server') {
            steps {
                script {
                    sshagent(['spark-server-ssh-credential-id']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no hr295@${SPARK_SERVER} << EOF
                        set -e
                        echo "Starting Spark job on remote server..."

                        export SPARK_HOME=${SPARK_HOME}
                        export PATH=\$SPARK_HOME/bin:\$PATH

                        ${SPARK_HOME}/bin/spark-submit \\
                            --master local[*] \\
                            --driver-memory 4g \\
                            --executor-memory 4g \\
                            --jars ${JDBC_JAR_PATH} \\
                            ${SPARK_SCRIPT_PATH}

                        echo "Spark job completed successfully."
                        exit
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
            echo "Spark job execution failed."
        }
    }
}
