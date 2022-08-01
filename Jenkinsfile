
import groovy.json.JsonSlurper
access_token = ''
refresh_token = ''
user_id = ''
logged = false
snippet = ''

Map login(username, password) {
    def post_login = new URL("http://django:8000/login/").openConnection()
    def body = '{"username":' + '"' + username + '"' + "," + '"password":' + '"' + password + '"}'
    post_login.setRequestMethod("POST")
    post_login.setDoOutput(true)
    post_login.setRequestProperty("Content-Type", "application/json")
    post_login.setRequestProperty("Accept", "application/json")
    post_login.getOutputStream().write(body.getBytes("UTF-8"))
    if (post_login.getResponseCode() == 200) {
      String response = post_login.getInputStream().getText()
      JsonSlurper slurper = new JsonSlurper()
      Map parsedJson = slurper.parseText(response)
      access_token = parsedJson.access
      refresh_token = parsedJson.refresh
      user_id = parsedJson.user_id
      return [isClear:true, reason:"Login successfull"]
    } else {
        return [isClear:false, reason: "Login error"]
      }
}

node {
    stage('Get snippet') {
        git branch: 'main', url: 'https://github.com/max45556/PipelineWithDjango.git'
        def file = new File("/var/jenkins_home/workspace/DjangoPipe/snippet.py")
        snippet = file.text
        println("Snippet to analyze: \n\n" + snippet)
    }
    stage('Logging') {
      def result = login('admin', 'admin1212')
      println(result.reason)
      if (result.isClear) {
        logged = true
        println("Access: " + access_token)
        println("Refresh: " + refresh_token)
        println("user_id: " + user_id)
        }
      }
    if (logged) {
      stage('ciccio') {
        def get = new URL("http://django:8000/help").openConnection();
        def getRC = get.getResponseCode();
        println(getRC);
        if(getRC.equals(200)) {
          println(get.getInputStream().getText())
          }
        }
      }
}
