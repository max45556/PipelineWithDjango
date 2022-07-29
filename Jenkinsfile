pipeline {
    agent any
    stages {
        stage('Build with agent1') {
          steps {
              sh 'cat /etc/environment'
              sh 'ls -l'
              sh 'pwd'
              sh 'mvn clean package -DskipTests'
              sh 'mvn spotbugs:spotbugs'
              }
        }
        stage('Saving jar') {
          agent { label 'agent1' }
          steps {
              sh 'mvn install deploy -DskipTests'
              }
        }
        stage('Moving jar file') {
          agent { label 'agent1' }
          steps {
              sh 'pwd'
              sh 'ls -l'
              sh 'cp -r target /home/v_data'
              sh 'ls -l /home/v_data'
            }
        }
        stage('Running on agent2') {
            agent { label 'agent2' }
            steps {
                sh 'echo Hi from agent2'
                sh 'java --version'
                sh 'ls -l /home/v_data'
                sh 'PID=$(jps -v | grep webgoat | cut -d " " -f1) && if [ -z "$PID" ]; then echo niente da eliminare; else kill $PID; fi'
                sh 'JENKINS_NODE_COOKIE=dontKillMe nohup java -jar -Dwebgoat.host=0.0.0.0 /home/v_data/target/webgoat-8.2.3-SNAPSHOT.jar &'
                sh 'echo $(jps -v | grep webgoat | cut -d " " -f1)'
                sh 'echo GO TO 127.0.0.1:8888/WebGoat'
            }
        }
        stage('Zaproxy') {
            steps {
              sh 'docker run -d --name zap_agent --network jenkins_bridge -v v_report:/zap/wrk/:rw -t zap_customize'
              sh 'docker exec zap_agent ls -l /zap/wrk/'
              sh 'docker exec zap_agent zap-full-scan.py -I -j -m 10 -T 60 -t http://agent2:8080/WebGoat --hook=/zap/auth_hook.py -r report.html -x report.xml -J report.json -z "auth.loginurl=http://agent2:8080/WebGoat/login auth.username="developer" auth.password="password" auth.auto=1"'
              sh 'docker stop zap_agent'
              sh 'docker rm zap_agent'
          }
        }
        stage('Sending report') {
          agent { label 'agent1' }
          steps {
              sh 'ls -l'
              sh 'pwd'
              sh 'ls -l /home/v_report'
              sh 'mvn sonar:sonar \
              -Dsonar.host.url=http://sonarqube:9000 \
              -Dsonar.java.spotbugs.reportPaths=\"target/spotbugsXml.xml\" \
              -Dsonar.login=sqp_28d8ae58794d33aa2532755208d8b193a6fa9456 \
              -Dsonar.projectKey=wg \
              -Dsonar.zaproxy.reportPath=/home/v_report/report.xml \
              -Dsonar.zaproxy.htmlReportPath=/home/v_report/report.html'
              }
        }
    }
}
