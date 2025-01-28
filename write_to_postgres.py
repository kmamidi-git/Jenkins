pipeline {
    agent any

    environment {
        SPARK_HOME = '/home/hr295/spark'
        SPARK_SCRIPT_PATH = '/home/hr295/spark_files/test_job.py' // Update this to the correct file path
        SPARK_SERVER = '192.168.1.77' // Remote server IP
        JDBC_JAR_PATH = '/home/hr295/spark/jars/postgresql-42.6.0.jar'
        CSV_FILE_PATH = 'file:///home/hr295/reporter_dt.csv'
        PGSQL_URL = 'jdbc:postgresql://192.168.1.77:5432/sample_database'
        PGSQL_USER = 'postgres'
        PGSQL_PASSWORD = 'access'
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

                        # Ensure Spark and necessary configurations are available
                        export SPARK_HOME=${SPARK_HOME}
                        export PATH=\$SPARK_HOME/bin:\$PATH

                        # Execute the Spark job
                        ${SPARK_HOME}/bin/spark-submit \\
                            --master local[*] \\
                            --driver-memory 4g \\
                            --executor-memory 4g \\
                            --jars ${JDBC_JAR_PATH} \\
                            ${SPARK_SCRIPT_PATH} \\
                            ${CSV_FILE_PATH} ${PGSQL_URL} ${PGSQL_USER} ${PGSQL_PASSWORD}

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
