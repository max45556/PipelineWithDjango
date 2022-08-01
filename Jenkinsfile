
import groovy.json.JsonSlurper
String access_token = ''
String refresh_token = ''
String user_id = ''

Map login(username, password) {
    def post_login = new URL("http://django:8000/login/").openConnection();
    def body = '{"username":' + '"' + username + '"' + "," + '"password":' + '"' + password + '"}'
    post_login.setRequestMethod("POST")
    post_login.setDoOutput(true)
    post_login.setRequestProperty("Content-Type", "application/json")
    post_login.setRequestProperty("Accept", "application/json")
    post_login.getOutputStream().write(body.getBytes("UTF-8"));
    if (post_login.getResponseCode() == 200) {
      String response = post_login.getInputStream().getText();
      JsonSlurper slurper = new JsonSlurper()
      Map parsedJson = slurper.parseText(response)
      access_token = parsedJson.access
      refresh_token = parsedJson.refresh
      user_id = parsedJson.user_id
      return [isClear:true, reason:"GOOD"]
      } else {
        println("POCO MALE")
        return [isClear:false, reason:"ciao"]
        }
      }

node {
    stage('Preparation') {
        git branch: 'main', url: 'https://github.com/max45556/PipelineWithDjango.git'
        def file = new File("/var/jenkins_home/workspace/DjangoPipe/snippet.py")
        String fileContent = file.text
        println("Snippet to analyze: \n" + fileContent)
    }
    stage('Login') {
      def result = login('admn', 'admin1212')
      if (result.isClear) {
        println(result.reason)
      }
    }
    stage('ciccio') {
    def get = new URL("http://django:8000/help").openConnection();
    def getRC = get.getResponseCode();
    println(getRC);
    if(getRC.equals(200)) {
        println(get.getInputStream().getText());
        }
    }
}
