
import groovy.json.JsonSlurper
access_token = ''
refresh_token = ''
user_id = ''
logged = false
snippet = ''

def get_user_snippets() {
  def get_request = new URL("http://django:8000/snippets/").openConnection();
  get_request.setRequestMethod("GET")
  get_request.setRequestProperty("Content-Type", "application/json")
  get_request.setRequestProperty("Authorization", "Bearer " + access_token)
  def getRC = get_request.getResponseCode();
  println(getRC);
  if(getRC.equals(200)) {
    println(get_request.getInputStream().getText())
    }
}

Map language_identification() {
    def post_language = new URL("http://django:8000/snippets/detect/").openConnection()
    def body = '{"code":' + '"' + snippet + '"}'
    post_language.setRequestMethod("POST")
    post_language.setDoOutput(true)
    post_language.setRequestProperty("Content-Type", "application/json")
    post_language.setRequestProperty("Accept", "application/json")
    post_language.setRequestProperty("Authorization", "Bearer " + access_token)
    post_language.getOutputStream().write(body.getBytes("UTF-8"))
    print(post_language.getResponseCode())
    String response = post_language.getInputStream().getText()
    JsonSlurper slurper = new JsonSlurper()
    Map parsedJson = slurper.parseText(response)
    println("DIGEL " + parsedJson)
}

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
        stage('See user Snippet') {
          get_user_snippets()
        }
        stage('Identify language') {
          language_identification()
        }
      }

  }
